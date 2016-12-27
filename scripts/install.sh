apt-get update
apt-get install -y vim python-dev python-pip
pip install spidev requests
mkdir /home/pi/.ssh || true
echo -e 'Host github.com\\n\\tStrictHostKeyChecking no\\n' > /home/pi/.ssh/config
rm -rf /home/pi/SPI-Py || true
git clone https://github.com/lthiery/SPI-Py /home/pi/SPI-Py
cd /home/pi/SPI-Py && python setup.py install
