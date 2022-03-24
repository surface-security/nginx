ARG BASE_IMAGE=nginx:1.21.6-alpine
FROM ${BASE_IMAGE}

RUN --mount=type=bind,src=/install_helpers,target=/install_helpers \
    /install_helpers/check.sh

ARG TARGETPLATFORM
ARG USESPRIG
RUN --mount=type=bind,src=/install_helpers,target=/install_helpers \
    /install_helpers/confgen.sh "$TARGETPLATFORM" "$USESPRIG"

COPY 20-envsubst-on-templates.sh /docker-entrypoint.d/20-envsubst-on-templates.sh
