## Connection to firebase

1. Create Firebase project
   -    [firebase](https://console.firebase.google.com)


2. After creating a project 

   - Click on `project Settings` then navigate to `service accounts` tab as shown below.
   - 
![](/Pulmo-AI/static/auth/step1.png)


3. scroll down and click on `Generate nw private key`

   - rename the Json file `firestore-creds.json`
   - place it inside `./Pulmo-AI/Creds/`
   - 
![](/Pulmo-AI/static/auth/step2.png)



4. Scroll up and click on `General`
   
    - wait a bit for it load

![](/Pulmo-AI/static/auth/step3.png)


1. Scroll down and select on `Config`

![](/Pulmo-AI/static/auth/step4.png)

6. paste config content in a json file `config.json`
   
   - place it inside `./Pulmo-AI/Creds/`


![](/Pulmo-AI/static/auth/step5.png)

7. your `config.json` should look like this
```json
{
    "apiKey": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "authDomain": "XXXXXXXXXXXXXXXXXXXXXXXXX",
    "projectId": "XXXXXXXXXXXXXXXXXXX",
    "storageBucket": "XXXXXXXXXXXXXXXXXXXXXXX",
    "messagingSenderId": "XXXXXXXXXXXXXXXXXXXX",
    "appId": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "measurementId": "XXXXXXXXXXXXXXX",
    "databaseURL": "XXXXXXXXXXXXXXXXXXXXXXXXXXX"
}
```
>DONT SHARE YOUR CREDENTIALS WITH ANYONE