## Table of contents
- [Table of contents](#table-of-contents)
- [Buffet meaning](#buffet-meaning)
- [What is doing our programm?](#what-is-doing-our-programm)
- [How To run the app?](#how-to-run-the-app)
- [How To use the app?](#how-to-use-the-app)
- [Have a look on programm database](#have-a-look-on-programm-database)
- [Technologies](#technologies)
- [Contributors](#contributors)
- [Achievement](#achievement)
- [Contact](#contact)
- [Conclusion](#conclusion)

## Buffet meaning
I don't know how the schools in your country are, but in my country there is a small shop in the schools that sells different food items to the students. We call these shops buffets.

![buffet3](https://github.com/user-attachments/assets/0aa28949-c9d2-4d87-ba2e-2b3d3f014628)

This is a buffet in school and students are waiting in queue for their turn.👆👆

## What is doing our programm?
Ok! Now you know what is buffet, but what our app do in this shops?

We place a camera in the window or anywhere else that has a good view of the students' faces. Then we can use opencv modules for face detection and face recognition to register the students' faces in our database and recognize them next time.
After recognize them, we connect to their account. There they can charge their credit or buy products. We have a good and powerful log system too. I will explain more...
	
## How To run the app?
To run this programm, open terminal in the programm folder first and install packages with pip:
```
pip install -r requirments.txt
```
This may take some time due to the large amount of dependencies.

now you are ready to run the app with this command:
```
python3 main.py
```

## How To use the app?
The first time you run the app, it may take some time to download the extensions and create the base directory.

When download is finished, you see this page:

![screenshot_from_register_final](https://github.com/user-attachments/assets/a9ceada8-3251-447f-a314-9ff0d2c318ab)

This page is for enter seller(not buyer or student), but you don't have account yet. Then click `Register`.

Follow the steps for register, then You will be returned in the first page. Here you can enter to the account you created and access to the home page:

![home-final](https://github.com/user-attachments/assets/32ccd71c-fa19-48cb-bdeb-c6f981b637fc)

Your account is a seller account, not a buyer.
For create new buyers(students), we must register school, class and preferably product. All of this settings can be managed in this path: home page -> Settings -> Manage database:

![databasemanage-final](https://github.com/user-attachments/assets/0c55657d-1a95-4357-a3ad-2c9b1a98dd79)

We have 4 parts here:
* Schools: Manage schools.
* Classes: Manage classes.
* Products: Manage products.
* Users: Manage users(sellers).

In the programm, we have 3 level of user(seller):
* Creator: The first user(seller) registered into programm.
* Admin : A medium-level user(seller).
* Normal: Default level for each user(seller) except the first one(he/she is creator).

Creator can change level of other user from the Users page. Of course, these three levels have more differences that you will see them by explore in programm.

Now we have requirements for register a buyer. Let's do it from this path: home page -> register :

!![register-buyer-final](https://github.com/user-attachments/assets/f54a1682-bd7f-481f-8d6a-c6add92fff44)

After hit `Register` button, process starts and take a few secondes, then you will be returned to the home page.

For enter to the buyer account page, go to this path: home page -> enter. process starts and take a few secondes, then you can see the buyer account page:

![account-final](https://github.com/user-attachments/assets/7552507b-48c4-48f0-93d2-8611277b2d66)

[here](https://github.com/user-attachments/assets/dd188372-c146-44c3-9430-e2bbadb65787) is a product oriented purchase guide . 

For charge credit or price oriented purchase, hit the `Charge/import manually` button:

![calculator-final](https://github.com/user-attachments/assets/98d5385b-e4f7-405b-a492-5caae4037cec)

## Have a look on programm database 
In windows, base directory location is:
```
C:/BUFFET
```
and in linux is:
```
/home/your-username/BUFFET
```
2 folders are waiting here:
* `data`: Our programm data is here.
* `extensions`: Icon, font, algorithm and html pages are here.

In data folder:
* `database.db` file: The main database file. Have 5 tables:
  * buyers
  * users
  * schools_classes
  * logs
  * products
* `text` folder: Include language and theme.
* `trainer` folder: In this folder, there is only one file called `trainer.yml`, which is very important. Face features are here.

## Technologies 
* `python` version 3.12.3
* `opencv` version 4.10.0.84
* `opencv-contrib` version 4.10.0.84
* `kivy` version 2.3.0
* `kivymd`version 1.2.0
* `pygame` version version 2.6.0


## Contributors
* [mohammad hesam afzali](https://github.com/mhafzali) -> the front designer(kivy, kivymd and ...)
* [parsa safaie](https://github.com/parsasafaie) -> the back designer(opencv, sqlite3 and ...)

Thanks to all those who guided and supported us in this way


## Achievement
For the first time, our program was sent to the Khwarazmi Youth Festival, which is a big festival in Iran and holds competitions in various fields. Our program reached the first place in the province in this competition and participated in the national level judging, the results of which will be determined soon.

![jashnvare-final](https://github.com/user-attachments/assets/6356af82-3511-45fe-8877-6e5a22352175)

Logo of Khwarazmi Youth Festival👆👆

## Contact
ّf you have any Suggestion or criticism, we will be happy to hear:
* mohammadhesamafzali131415@gmail.com for front
* parsasafaie.2568@gmail.com for back 

## Conclusion
That's all. Thanks for reading this long README and the time you gave to this. Wish you success and happiness.

*BUFFET programm team*