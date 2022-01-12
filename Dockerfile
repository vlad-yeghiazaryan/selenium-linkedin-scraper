# Seting the python env from IBM image
FROM ibmfunctions/action-python-v3.7
RUN apt-get update; apt-get clean

RUN apt-get install -y libglib2.0-0=2.50.3-2 \
    libnss3=2:3.26.2-1.1+deb9u1 \
    libgconf-2-4=3.2.6-4+b1 \
    libfontconfig1=2.11.0-6.7+b1

# Install Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list
# Install Chrome.
RUN apt-get update && apt-get -y install google-chrome-stable

# Add the python scripts
RUN mkdir -p ./dist
RUN mkdir -p ./dist/drivers
WORKDIR ./dist
COPY __main__.py linkedinScraper.py requirements.txt .env .
COPY drivers/chromedriverLinux64 ./drivers

# Import python libs
RUN pip install --upgrade pip
RUN pip install -r requirements.txt