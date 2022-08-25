# CS50w Capstone - Stocks Manager

## Description

This project is a stock manager website, where you can search and keep track of your stocks and also read some business news. I believe that it might be helpful for the investors to keep track of some stocks and their performance.

### Here you are able to:
- Read some stock market news;
- Add stocks to your watchlist;
- Add your transactions (buy or sell operations);
- Keep track of your portfolio based on your transactions (quantity, rentability, average price, etc.);
- and search for a specific stock graphic.

### Distinctiveness and Complexity

Considering its usability and purpose, this project is unique among all tasks assigned during the course.
To build it, I used all languages (HTML, CSS, Scss, Python, Javascript) and frameworks (Django) learned during this period. It also uses some API services to get data for the news and for the stocks quotation/graphic, and I styled it (with a little help from bootstrap) to be nice looking and responsive as well. Therefore, I believe it satisfies the 'distinctiveness and complexity' requirements.

## Project Files
All project created/required files are under */stocks_manager*.

### Python files

- #### views.py
The part of the project that receives and returns Http responses and modifies the database.

- #### urls.py
In this file all the urls are declared.

- #### models.py
This file is responsible for the database table creations, in my case there are three tables: User, Transactions and Watchlist.

### Templates

- #### login.html/register.html
Page where the user is able to register and login into the site.

- #### layout.html
Is the base of other html files, it includes a navbar with tags for the user navigates through the website and register/login/logout.

- #### index.html
Page that displays to the user some business news (using [News API](https://newsapi.org/)) and some stocks quotations (using [IEX Cloud API](https://iexcloud.io/)) on the top of the page.

- #### portfolio.html
Shows the user's stocks based on his transactions.
Here the user can see his stock's performance, number of shares, total position and the actual price (using [IEX Cloud API](https://iexcloud.io/)).

- #### watchlist.html
Here the user is able to add stocks and keep track of its current price.

- #### transactions.html
In this page the user can add his transactions, informing the stock symbol, price, number of shares, operation (buy or sell) and the date.

- #### chart.html
Here javascript was used to build a stock chart. The user can type in the form a stock symbol and it will return a graphic of the price variation in the last 30 days.

### Static

- #### styles.scss
File used to add some style to the website and to control some animations (carousel, loading icon, responsiveness).

- #### styles.css/styles.css.map
Scss auto-generated files.

### Templatetags

- #### stock_tags.py
In this file I added some specific django templatetags, used to show the user's rentability and to multiply some value to show it's percent variation.

## Running the project
To run the project, you need to install the packages listed on requirements.txt:

```
pip install -r requirements.txt
```
then you need to migrate:
```
python manage.py makemigrations

python manage.py migrate
```
and finally, you can run the app:
```
python manage.py runserver
```

## Additional information
I recommend you to create your own API keys on [IEX Cloud API](https://iexcloud.io/) and [News API](https://newsapi.org/).

### Youtube screencast
💻 [Check out here!](https://youtu.be/7PZad0DyzcM)
