#!/usr/bin/env python
"""
github action helper to expand matrix options

based on https://github.com/fopina/docker-wine-python/blob/main/expand.py
"""
from ensurepip import version


DOCKER_IMAGE = "fopina/wine-python"


class Error(Exception):
    """command error"""

    def __str__(self):
        return "::error title=workflow::%s" % self.args[0]


def handle(tag, image="", line=None, verbose=False, extra=None):
    """
    >>> handle('1.19')
    Traceback (most recent call last):
    ...
    expand.Error: ::error title=workflow::use full nginx version, including patch version, ie, 1.19.1
    >>> handle('1.19.1-a')
    Traceback (most recent call last):
    ...
    expand.Error: ::error title=workflow::build (after -) must be a number, if any
    >>> handle('1.19.1')
    ::set-output name=base_image::1.19.1
    ::set-output name=output_tags:::1.19,:1.19.1
    >>> handle('1.19.1', extra='nosprig')
    ::set-output name=base_image::1.19.1
    ::set-output name=output_tags:::1.19-nosprig,:1.19.1-nosprig
    >>> handle('1.19.1-1')
    ::set-output name=base_image::1.19.1
    ::set-output name=output_tags:::1.19,:1.19.1,:1.19.1-1
    >>> handle('1.19.1', line='alpine')
    ::set-output name=base_image::1.19.1-alpine
    ::set-output name=output_tags:::1.19-alpine,:1.19.1-alpine
    >>> handle('1.19.1-2', line='other')
    ::set-output name=base_image::1.19.1-other
    ::set-output name=output_tags:::1.19-other,:1.19.1-other,:1.19.1-2-other
    >>> handle('1.19.1-2', line='other', extra='nosprig')
    ::set-output name=base_image::1.19.1-other
    ::set-output name=output_tags:::1.19-nosprig-other,:1.19.1-nosprig-other,:1.19.1-2-nosprig-other
    """
    nginx_version, *parts = tag.split("-")
    if nginx_version.count(".") != 2:
        raise Error("use full nginx version, including patch version, ie, 1.19.1")
    if len(parts) > 1:
        raise Error("too many - in that tag name!!!")
    if parts:
        build = parts[0]
        if not build.isdigit():
            raise Error("build (after -) must be a number, if any")
    else:
        build = None

    def outprint(var, value):
        print("::set-output name=%s::%s" % (var, value))
        if verbose:
            print("%s = %s" % (var, value))

    out_tags = [nginx_version.rsplit(".", 1)[0], nginx_version]
    if build:
        out_tags.append("%s-%s" % (nginx_version, build))
    if extra:
        out_tags = ["%s-%s" % (ot, extra) for ot in out_tags]
    base_image = nginx_version
    if line is not None:
        base_image = "%s-%s" % (nginx_version, line)
        out_tags = ["%s-%s" % (ot, line) for ot in out_tags]

    outprint("base_image", base_image)
    full_tags = ["%s:%s" % (image, ot) for ot in out_tags]
    outprint("output_tags", ",".join(full_tags))


def main():
    import argparse
    import sys

    parser = argparse.ArgumentParser(
        description="From the target github tag name, derives all image tags to be used"
    )
    parser.add_argument("tag", type=str, help="target tag name")
    parser.add_argument(
        "-i", "--image", type=str, default="image", help="image name (for output tags)"
    )
    parser.add_argument(
        "-l", "--line", type=str, help="variant (if any), such as alpine"
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="verbose output")
    parser.add_argument(
        "-e", "--extra", type=str, help="Extra label for output tags (after build)"
    )
    args = parser.parse_args()
    try:
        handle(
            args.tag,
            image=args.image,
            line=args.line,
            verbose=args.verbose,
            extra=args.extra,
        )
    except Error as e:
        print(e, file=sys.stderr)
        exit(2)


if __name__ == "__main__":
    main()
