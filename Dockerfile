# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables to reduce the output of debconf
ENV DEBIAN_FRONTEND=noninteractive

# Install necessary dependencies
RUN apt-get update && \
    apt-get install -y \
    git \
    wget \
    unzip \
    xvfb \
    libxi6 \
    libgconf-2-4 \
    curl \
    gnupg \
    gnupg2 \
    gnupg1 \
    && rm -rf /var/lib/apt/lists/*

# Install Google Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

# Install Chromedriver - Set Chromrdriver version as version of chrome installed
RUN CHROMEDRIVER_VERSION=$(google-chrome -version | sed 's/Google Chrome \([0-9.]*\).*/\1/') && \  
    wget -O /tmp/chromedriver.zip https://storage.googleapis.com/chrome-for-testing-public/${CHROMEDRIVER_VERSION}/linux64/chromedriver-linux64.zip && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    mv /usr/local/bin/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver && \
    chmod +x /usr/local/bin/chromedriver && \
    rm -rf /tmp/chromedriver.zip /usr/local/bin/chromedriver-linux64

# Export ChromeDriver path to PATH
ENV PATH="/usr/local/bin/chromedriver-linux64/chromedriver:${PATH}"

# Set the working directory in the container
WORKDIR /app

# Clone the repository
RUN git clone https://github.com/inert14/AutomateNotificationProcess.git /app

# Copy files
COPY credentials.json /app/
COPY token.json /app/
COPY /userdata/ /app/userdata/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 5000

# Command to run the Flask API with Gunicorn
# CMD ["gunicorn", "-w", "1", "--bind", "0.0.0.0:5000", "InitialWhatsappLogin:app", "--timeout", "120"]
CMD ["gunicorn", "-k", "AutomateNotificationProcess.CustomGeventWorker", "--bind", "0.0.0.0:5000", "AutomateNotificationProcess:app"]
