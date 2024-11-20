# **Technical Documentation for Flask E-commerce Application**

---

## 1. **Introduction**

This application is based on the Flask framework and serves as a complete e-commerce platform. Users can register, log in, browse products, add them to their cart, place orders, and process payments. Administrators can manage products, categories, and monitor orders. After each successful purchase by a user, the quantity of products in stock is reduced to the current level.

---

## 2. **Requirements**

The following packages and libraries are required for the application to function properly:

- **Operating System**: Linux Ubuntu
- **Python 3.11.10**: The Python version for running the application.
- **Flask 3.0.3**: A framework for handling HTTP requests and managing sessions.
- **Flask-Login 0.6.3**: User session management.
- **Werkzeug 3.0.3**: A tool for secure password hashing.
- **Stripe 2.49.0**: Online payment processing.
- **Flask-SQLAlchemy 3.1.1**: Integration with SQL databases.
- **Flask-CKEditor 1.0.0**: Integration of the CKEditor text editor with Flask.
- **Bootstrap-Flask 2.4.1**: User interface styling.
- **Flask-WTF 1.2.1**: Form handling with validation.
- **WTForms 2.3.3**: Extension for form validation and creation.
- **Bleach 6.1.0**: Library for cleaning and validating HTML data.

---

## 3. **Environment Setup**

Before running the application, it is necessary to create a virtual environment and install all dependencies. Follow the steps below:

### **Steps:**

1. **Install Miniconda (if you haven't already):**
   - Miniconda is a lightweight version of Anaconda that allows you to manage packages and environments in Python. You can download Miniconda from the [official site](https://docs.conda.io/en/latest/miniconda.html) and follow the installation instructions.

2. **Create a new virtual environment:**
   - Open a terminal and run the following command to create a new environment named `myenv` (you can replace `myenv` with any name):
     ```bash
     conda create --name myenv python=3.11
     ```

3. **Activate the environment:**
   - After creating the environment, activate it with the command:
     ```bash
     conda activate myenv
     ```

4. **Install all dependencies:**
   - Make sure you are in the active environment, then install the necessary packages. You can do this using the `requirements.txt` file if it exists:
     ```bash
     pip install -r requirements.txt
     ```

5. **Deactivate the environment after finishing work:**
   - Once you are done working in the environment, you can deactivate it:
     ```bash
     conda deactivate
     ```

### **Benefits of Using Miniconda:**
- **Dependency Management:** Miniconda simplifies package installation and management, eliminating dependency issues.
- **Creating and Managing Environments:** You can easily create, activate, and deactivate different virtual environments, allowing for project separation.
- **Support for Different Python Versions:** You can have different Python versions installed in various environments.

By following these steps, you will be ready to work on your application in a well-configured environment!

---


## 4. **Stripe Webhook - Local Configuration**

To run the Stripe Webhook locally, follow these steps:

1. **Install Stripe CLI**  
   Stripe CLI is a tool for testing and managing Stripe Webhooks. To install Stripe CLI on Linux Ubuntu, use the following command:  
   ```bash
   curl -fsSL https://stripe.com/install.sh | bash
   ```

2. **Log in to Stripe CLI**
   After installation, log in to your Stripe account using: 
   ```bash
   stripe login
   ```
   
3. **Run the Stripe Webhook locally**
   To forward Stripe Webhook notifications to your local server, use the command:  
   ```bash
   stripe listen --events checkout.session.completed \
   --forward-to localhost:4242/webhook
   ```

4. **Configure the Webhook Secret Key in the Application**
   Stripe generates a Webhook secret key when running Stripe CLI. Save this key and add it to the environment variables in your application, e.g., in the .env file: 
   ```bash
   STRIPE_WEBHOOK_SECRET=whsec_xxxxxxxxxxxxxx
   ```






# **Dokumentacja Techniczna Aplikacji Flask E-commerce**

<a name="wprowadzenie" id="#wprowadzenie"></a>
## 1. **Wprowadzenie**

Aplikacja oparta na frameworku Flask, która stanowi kompletną platformę e-commerce. Użytkownicy mogą rejestrować się, logować, przeglądać produkty, dodawać je do koszyka, składać zamówienia i realizować płatności. Administratorzy mogą zarządzać produktami, kategoriami oraz monitorować zamówienia.
Po każdym udanym zakupie przez użytkownika ilość produktów w magazynie jest redukowana do stanu
aktualnego.

---

<a name="wymagania"></a>
## 2. **Wymagania**

Do poprawnego działania aplikacji wymagane są następujące pakiety i biblioteki:

- **System operacyjny**: Linux Ubuntu
- **Python 3.11.10**: Wersja Python do uruchamiania aplikacji.
- **Flask 3.0.3**: Framework do obsługi zapytań HTTP i zarządzania sesjami.
- **Flask-Login 0.6.3**: Zarządzanie sesjami użytkowników.
- **Werkzeug 3.0.3**: Narzędzie do obsługi bezpiecznego haszowania haseł.
- **Stripe 2.49.0**: Obsługa płatności online.
- **Flask-SQLAlchemy 3.1.1**: Integracja z bazą danych SQL.
- **Flask-CKEditor 1.0.0**: Integracja edytora tekstowego CKEditor z Flask.
- **Bootstrap-Flask 2.4.1**: Stylizacja interfejsu użytkownika.
- **Flask-WTF 1.2.1**: Obsługa formularzy z walidacją.
- **WTForms 2.3.3**: Rozszerzenie do walidacji i tworzenia formularzy.
- **Bleach 6.1.0**: Biblioteka do czyszczenia i walidacji danych HTML.

---

<a name="konfiguracja-środowiska"></a>
## 3. **Konfiguracja Środowiska**

Przed uruchomieniem aplikacji konieczne jest utworzenie wirtualnego środowiska i zainstalowanie wszystkich zależności. W tym celu należy postępować zgodnie z poniższymi krokami:

### **Kroki:**

1. **Zainstaluj Miniconda (jeśli jeszcze go nie masz):**
   - Miniconda to lekka wersja Anacondy, która pozwala na zarządzanie pakietami i środowiskami w Pythonie. Możesz pobrać Minicondę ze strony [oficjalnej](https://docs.conda.io/en/latest/miniconda.html) i postępować zgodnie z instrukcjami instalacji.

2. **Utwórz nowe środowisko wirtualne:**
   - Otwórz terminal i uruchom poniższe polecenie, aby utworzyć nowe środowisko z nazwą `myenv` (możesz zastąpić `myenv` dowolną nazwą):
     ```bash
     conda create --name myenv python=3.11
     ```
   - Możesz także zainstalować inne wersje Pythona, zmieniając `3.9` na wersję, której potrzebujesz.

3. **Aktywuj środowisko:**
   - Po utworzeniu środowiska, aktywuj je poleceniem:
     ```bash
     conda activate myenv
     ```

4. **Zainstaluj wszystkie zależności:**
   - Upewnij się, że znajdujesz się w aktywnym środowisku, a następnie zainstaluj potrzebne pakiety. Możesz to zrobić, korzystając z pliku `requirements.txt`, jeśli taki istnieje:
     ```bash
     pip install -r requirements.txt
     ```

5. **Zdezaktywuj środowisko po zakończeniu pracy:**
   - Po zakończeniu pracy w środowisku, możesz je dezaktywować:
     ```bash
     conda deactivate
     ```

### **Zalety korzystania z Minicondy:**
- **Zarządzanie zależnościami:** Miniconda ułatwia instalację i zarządzanie pakietami, eliminując problemy z zależnościami.
- **Tworzenie i zarządzanie środowiskami:** Możesz łatwo tworzyć, aktywować i dezaktywować różne środowiska wirtualne, co pozwala na separację projektów.
- **Wsparcie dla różnych wersji Pythona:** Możesz mieć różne wersje Pythona zainstalowane w różnych środowiskach.

Dzięki tym krokom będziesz gotowy do pracy nad swoją aplikacją w dobrze skonfigurowanym środowisku!

---

<a name="konfiguracja-webhook"></a>
## 4. **Stripe Webhook - Konfiguracja Lokalna**

Aby uruchomić Stripe Webhook lokalnie, wykonaj poniższe kroki:

1. **Zainstaluj Stripe CLI**  
   Stripe CLI jest narzędziem do testowania i obsługi Stripe Webhooków. Aby zainstalować Stripe CLI na Linux Ubuntu, użyj poniższego polecenia:  
   ```bash
   curl -fsSL https://stripe.com/install.sh | bash
   ```

2. **Zaloguj się do Stripe CLI**
   Po instalacji zaloguj się na swoje konto Stripe::  
   ```bash
   stripe login
   ```
   
3. **Uruchom Stripe Webhook lokalnie**
   Aby przekierować powiadomienia Webhook z Stripe na lokalny serwer, użyj polecenia:  
   ```bash
   stripe listen --events checkout.session.completed \
   --forward-to localhost:4242/webhook
   ```

4. **Skonfiguruj klucz Webhook w aplikacji:**
   Stripe generuje klucz Webhook podczas uruchamiania Stripe CLI. Zapisz ten klucz i dodaj go do zmiennych środowiskowych w aplikacji, np. w pliku .env:  
   ```bash
   STRIPE_WEBHOOK_SECRET=whsec_xxxxxxxxxxxxxx
   ```


