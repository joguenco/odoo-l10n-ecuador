FROM python:3.12-slim-bookworm

SHELL ["/bin/bash", "-xo", "pipefail", "-c"]

# Generate locale C.UTF-8 for postgres and general locale data
ENV LANG en_US.UTF-8

# Retrieve the target architecture to install the correct wkhtmltopdf package
ARG TARGETARCH

# Install some deps, lessc and less-plugin-clean-css, and wkhtmltopdf

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive \
    apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        dirmngr \
        fonts-noto-cjk \
        gnupg \
        libssl-dev \
        node-less \
        npm \
        git \
        python3-dev \
        python3-magic \
        python3-num2words \
        python3-odf \
        python3-pdfminer \
        python3-pip \
        python3-phonenumbers \
        python3-pyldap \
        python3-qrcode \
        python3-renderpm \
        python3-setuptools \
        python3-slugify \
        python3-vobject \
        python3-watchdog \
        python3-xlrd \
        python3-xlwt \
        python3-psycopg2 \
        python3-ldap \
        libldap2-dev \
        libsasl2-dev \
        ldap-utils \
        tox \
        lcov \
        valgrind \
        gcc \
        build-essential \
        python3-gevent \
        xz-utils \
        libpq-dev \
        libcairo2-dev \
        libjpeg-dev \
        libgif-dev \
        postgresql-client && \
    if [ -z "${TARGETARCH}" ]; then \
        TARGETARCH="$(dpkg --print-architecture)"; \
    fi; \
    WKHTMLTOPDF_ARCH=${TARGETARCH} && \
    case ${TARGETARCH} in \
    "amd64") WKHTMLTOPDF_ARCH=amd64 && WKHTMLTOPDF_SHA=e9f95436298c77cc9406bd4bbd242f4771d0a4b2  ;; \
    "arm64")  WKHTMLTOPDF_SHA=77bc06be5e543510140e6728e11b7c22504080d4  ;; \
    "ppc64le" | "ppc64el") WKHTMLTOPDF_ARCH=ppc64el && WKHTMLTOPDF_SHA=5312d7d34a25b321282929df82e3574319aed25c  ;; \
    esac \
    && curl -o wkhtmltox.deb -sSL https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-3/wkhtmltox_0.12.6.1-3.bookworm_${WKHTMLTOPDF_ARCH}.deb \
    && echo ${WKHTMLTOPDF_SHA} wkhtmltox.deb | sha1sum -c - \
    && apt-get install -y --no-install-recommends ./wkhtmltox.deb \
    && rm -rf /var/lib/apt/lists/* wkhtmltox.deb


# Install rtlcss (on Debian buster)
RUN npm install -g rtlcss

# Install Odoo
RUN adduser --disabled-password --home /opt/odoo --gecos '' odoo
RUN mkdir /etc/odoo && mkdir /tmp/odoo/
RUN git clone --depth=1 --branch=18.0 https://github.com/odoo/odoo.git /opt/odoo/server
RUN pip3 install --upgrade pip
RUN cd /opt/odoo/server && pip3 install -r requirements.txt
RUN pip3 install rlpycairo
RUN pip3 install phonenumbers
RUN pip3 install pyOpenSSL==24.0.0


# Copy entrypoint script and Odoo configuration file
COPY ./entrypoint.sh /
COPY ./odoo.conf /etc/odoo/

# Set permissions and Mount /var/lib/odoo to allow restoring filestore and /mnt/extra-addons for users addons
RUN chown odoo /etc/odoo/odoo.conf \
    && mkdir -p /mnt/extra-addons \
    && mkdir -p /var/lib/odoo \
    && chown -R odoo /mnt/extra-addons \
    && chown -R odoo /var/lib/odoo
VOLUME ["/var/lib/odoo", "/mnt/extra-addons"]

# Install Odoo modules
RUN git clone --depth=1 --branch=18.0 https://github.com/joguenco/odoo-l10n-ecuador.git /mnt/extra-addons
RUN cd /mnt/extra-addons && pip3 install -r requirements.txt


RUN ln -s /opt/odoo/server/odoo-bin /usr/bin/odoo-bin
# Expose Odoo services
EXPOSE 8069

# Set the default config file
ENV ODOO_RC /etc/odoo/odoo.conf

COPY wait-for-psql.py /usr/local/bin/wait-for-psql.py

# Set default user when running the container
USER odoo

ENTRYPOINT ["/entrypoint.sh"]
CMD ["odoo-bin"]
