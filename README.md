# 📢 Sagebot: Course News Telegram Bot

A web application that shares course-related updates via a Telegram bot. Administrators and instructors can post news or updates, which are automatically shared with subscribed users on Telegram.


---

## 🛠️ Badges

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.0.1-blue)
![Telegram Bot API](https://img.shields.io/badge/Telegram_Bot-API-lightblue)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange)

---

## 🎥 Demo

[Demo Video Link Here](Enter-Demo-URL)

---

## 📸 Project Screenshots

- **Landing Page**: A snapshot of the landing page with login and registration options.
-

- **Admin Panel**: Where administrators can post and manage course-related updates.
- 
- **Telegram Bot Updates**: Example of a Telegram message sent to users with course updates.

---

## ✨ Features

- **Admin Login**: Secure login for administrators.
- **Instructor Login**: Instructors can register and log in to post updates.
- **Post Course Updates**: Admins and instructors can post course information, which is sent to a Telegram group.
- **View Updates**: News and updates are stored in a database and can be viewed within the app.
- **Telegram Integration**: Automatically sends course-related messages to a specified Telegram group or channel.

---

## 🚀 Installation Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/KIPROTICHBETT53/Telegram-bot.git
   cd Telegram-bot

1.  **Set up the virtual environment**:
    ```bash
    `python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate```

2.  **Install dependencies**:

    bash


    `pip install -r requirements.txt`

3.  **Configure MySQL Database**:

    -   Ensure MySQL is running.
    -   Create a database named `sagebot`.
    -   Update the `app.config` details in `app.py` with your MySQL credentials.
4.  **Configure Telegram Bot**:

    -   Replace the bot token and chat ID with your Telegram bot token and target chat/group ID in the `post()` function.
5.  **Run the application**:

    bash

    `python app.py`

6.  **Access the application**: Open your browser and go to `http://127.0.0.1:5000`.

* * * * *

🤝 Contribution Guidelines
--------------------------

Contributions are welcome! Please fork this repository and submit a pull request.

1.  Fork the repo.
2.  Create a new branch (`git checkout -b feature-branch`).
3.  Commit your changes (`git commit -am 'Add new feature'`).
4.  Push to the branch (`git push origin feature-branch`).
5.  Create a new Pull Request.

* * * * *

🛠️ Technologies Used
---------------------

-   **Python** (3.8+)
-   **Flask** - Web framework
-   **MySQL** - Database
-   **Telegram Bot API** - Messaging
-   **HTML/CSS** - Frontend

* * * * *

📜 License
----------

This project is licensed under the MIT License. See the `LICENSE` file for details.

* * * * *

📞 Support
----------

For any questions or support, please contact:

-   **Elly Bett** - [LinkedIn](www.linkedin.com/in/elly-bett-5b2535247)
