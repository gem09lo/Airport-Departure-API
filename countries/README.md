# 🌍 REST Countries Searcher (Python CLI)

## 📝 Overview

This project is a simple Python CLI tool that allows users to search for countries by name and retrieve live data via the [REST Countries API](https://restcountries.com/). It demonstrates API interaction, exception handling, and testing using `pytest`.

**Note**: This is NOT part of the main Airports project. This project was a mini task from the Sigma Course to experiment with HTTP requests and APIs and is included in this repository to demonstrate skills.

---

## 🎯 Project Aims

- Practise using HTTP requests with external APIs.
- Build reusable exception classes for error handling.
- Write clean, modular code using functions.
- Implement TDD using `pytest` and `requests-mock`.

---

## 🧠 Key Concepts, Technologies & Features

- **HTTP Requests**: Uses `requests` to query the REST Countries API.
- **Error Handling**: Custom `APIError` class for graceful user feedback.
- **Test-Driven Development (TDD)**:
  - Unit tests with `pytest`
  - Mocking HTTP responses using `requests-mock`
- **Clean Code Principles**: Modular structure, meaningful function names.
- **CLI Interaction**: Repeated user input loop with friendly prompts.

---

## 🗂️ Project Structure
- [countries/]
   - `countries.py`: Main CLI logic and helper functions
   - `test_countries.py`: Unit tests for API calls

---

## ▶️ Running the Program
To launch the CLI tool:
`python countries.py`

Then enter a country name (e.g., France) when prompted. You'll receive a summary including:

- Common Name
- Currency
- Flag (emoji)

Example: 
`Search for a country: France
You searched for: France
Fetching...

Name: France
Currency: {'EUR': {'name': 'Euro', 'symbol': '€'}}
Flag: 🇫🇷`

---

## 🧪 Running the Tests
Run the test suite with:
`pytest test_countries.py`

All tests are written using pytest and use requests-mock to simulate API responses.

---

## ✅ Next Steps (Optional)
- Add more test cases (e.g., network errors, malformed responses).
- Format response output more cleanly.
- Handle case-insensitive input.