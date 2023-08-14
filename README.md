# Online Auction System with 3D Model Viewer using Django

Welcome to the Online Auction System with 3D Model Viewer built with Django! This project is designed to provide an interactive online auction platform integrated with a 3D model viewer. Users can participate in auctions and view 3D models of auction items.

## Technologies Used

- Python 3.9
- Django 3.2.7
- Bootstrap 4.1
- SQL Database

## Features

- **Luhn Algorithm Card Validation:** The system validates card numbers using the Luhn Algorithm. Learn more about the [Luhn Algorithm](https://www.geeksforgeeks.org/luhn-algorithm/). Example valid card numbers are provided.
- **3D Model Viewer:** Utilizes the model-viewer API for displaying 3D models of auction items. Only glb files are supported. Sample files are available in the `sample` directory.
- **Auction System:** Provides an interactive online auction system where users can participate in auctions and place bids.

## Getting Started

To get the project up and running on your system, follow these steps:

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/Tejas-Samel/Online-Auction-System-with-3d-model-viewer.git
   ```

2. **Create SQL Schema:**

   Create a SQL schema named `online-auction` in your database.

3. **Run Migrations:**

   Inside the terminal, navigate to the project directory and run the following commands:

   ```bash
   cd Online-Auction-System-with-3d-model-viewer
   python manage.py migrate
   ```

4. **Run the Server:**

   Start the Django development server:

   ```bash
   python manage.py runserver
   ```

5. **Access the Application:**

   Open your web browser and go to `http://127.0.0.1:8000/` to access the Online Auction System.

## 3D Model Viewer

For the 3D model viewer, the [model-viewer API](https://modelviewer.dev/) is utilized. Only glb files are supported for the 3D models. Sample glb files can be found in the `sample` directory.

## Luhn Algorithm Card Numbers

Here are some example card numbers that satisfy the Luhn Algorithm:

- 4532015112830366
- 6011514433546201
- 6771549495586802

---

![alt text](https://github.com/Tejas-Samel/Online-Auction-System-with-3d-model-viewer/blob/master/demopics/picture1.jpg)
![alt text](https://github.com/Tejas-Samel/Online-Auction-System-with-3d-model-viewer/blob/master/demopics/picture2.jpg)
![alt text](https://github.com/Tejas-Samel/Online-Auction-System-with-3d-model-viewer/blob/master/demopics/Vrmodel.jpg)

---

