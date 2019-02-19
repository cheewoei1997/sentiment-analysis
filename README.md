# Sentiment Analysis
The best practices for the development of a sentiment analysis app is practiced here.  

This application is bootstraped with Flask, but it has not been properly managed, so do expect a lot of messy code and unorganised files.

#### Documents
Copy away our hard work if you want to. It's our pleasure.  
* [Google Docs](https://docs.google.com/document/d/1Bo29K63w3szW4B2eWKKdsjU9nVy_VT2HqKmJlzkvz54/edit?usp=sharing)  
* [Google Slides](https://docs.google.com/presentation/d/1uxCehoqp5gMhGnISTCb7u-Pdx_21_lk6VRl3Yz_Ax2M/edit?usp=sharing)  

## Set Up
Here's how to get you started on copying all of the below tutorial codes. Run the below code to clone this repository onto your local computer.  
`git clone https://github.com/cheewoei1997/sentiment-analysis.git`

Once you've cloned, just navigate to the folder that you have cloned and you're all set.

### Set Up Your Environment
Start off by creating a virtual environment.  

#### Linux
```
virtualenv -p python3.6 venv
source venv/bin/activate
```  
#### Windows
```
virtualenv -p \path\to\python\python36 --distribute venv
.\venv\Scripts\activate
```  
#### MacOS
```
Sorry, but I'm not rich enough to figure this one out.
```

Download the necessary libraries.  
```
pip install -r requirements.txt
```

### Run Flask
Once you've installed all the necessary libraries, go ahead and run Flask to host your own server.
```
python run_sample_app.py
```

Hooray! You've deployed your lame Flask server. Why don't you navigate over to 
http://127.0.0.1:5000/ to check it out.  

Thank you all for coming to my TED Talk I hope this was worth your time.

## Credits
* Do Chen Hao
* Dr. Lee Chin Poo
