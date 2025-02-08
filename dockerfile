# Use Basic Image
FROM python:3.6

# Set Working Directory
WORKDIR /grapher

# Copy Local Code to The Image
COPY . /grapher

# Install Dependencies
RUN g++ -o metapath2vec/metapath2vec.so -shared -fPIC metapath2vec/metapath2vec.cpp
RUN pip install -r requirements.txt -i  https://mirrors.aliyun.com/pypi/simple/ 

# Set Startup Command
CMD ["python", "main.py"]