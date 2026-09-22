# Project Assignment: Student Expense Tracker Web Application

## 1. Project Overview
Design and build a full-stack local web application that allows students to record, manage, categorize, and analyze their daily personal expenses. The application must persist all data across sessions using an SQLite database and provide an interactive web interface built with Streamlit.

---

## 2. Technical Stack & Constraints
- **Programming Language**: Python 3.8+
- **User Interface**: Streamlit
- **Database**: SQLite3 (native `sqlite3` Python library)
- **Data Handling & Visualization**: Pandas and any standard charting library (Matplotlib, Seaborn, Altair, or Plotly)
- **No ORMs Allowed**: Use raw SQL statements for all database operations via `sqlite3`.

---

## 3. Functional Requirements

### 3.1. Database & Persistence Layer
Design and initialize an SQLite database named `expenses.db` with appropriate schema design, data types, and primary/foreign key constraints where applicable.

#### Required Data Attributes per Expense Record:
1. **ID**: Unique identifier.
2. **Date**: Date the expense occurred (`YYYY-MM-DD`).
3. **Category**: Category of the expense (e.g., *Food, Books & Supplies, Rent/Housing, Transportation, Entertainment, Utilities, Tuition, Miscellaneous*).
4. **Amount**: Monetary value (positive decimal/float).
5. **Payment Method**: Mode of payment (e.g., *Cash, Debit Card, Credit Card, UPI/Online Transfer*).
6. **Description / Notes**: Text description of the purchase.

---

### 3.2. User Interface & Feature Specifications

Your Streamlit application must feature a multi-section or sidebar navigation layout covering the following modules:

#### A. Expense Entry Module
- A form to log new expenses with input validation:
  - Date picker (defaulting to today's date).
  - Category dropdown menu.
  - Numeric input for the amount (prevent zero, negative, or blank submissions).
  - Dropdown/Radio buttons for payment method.
  - Text field for description/notes.
- A submission button that commits the record directly to the SQLite database and displays a visual confirmation or error state.

#### B. Records Management Module (View, Filter & Search)
- Display all recorded expenses in a tabular format.
- Multi-criteria filtering options:
  - **Date Range Filter**: Filter records between start and end dates.
  - **Category Filter**: Multi-select dropdown to view specific categories.
  - **Payment Method Filter**: Filter by payment mode.
  - **Search Bar**: Keyword search matching text within the description/notes field.
- Dynamic calculation and display of the **Total Filtered Expense Amount** and **Total Transaction Count**.

#### C. Record Update & Deletion Module
- Ability to select an existing record by its unique ID.
- Option to edit fields of a selected record and persist the changes back to SQLite.
- Option to permanently delete a selected record from the database with a confirmation prompt.

#### D. Analytics & Visualizations Dashboard
- **Monthly Summary**: Total expenditure grouped by month.
- **Category Breakdown**: A chart showing proportion/distribution of expenses across categories.
- **Payment Method Distribution**: A chart showing total money spent per payment method.
- **Daily/Weekly Trend**: A time-series chart showing spending trends over time.
- **Top Expenses**: A list or table highlighting the top $N$ highest expenses.

#### E. Monthly Budget Tracker (Bonus / Advanced Feature)
- Allow users to set a monthly budget threshold.
- Compare actual total expenses for the selected month against the set budget.
- Provide visual status indicators (e.g., Within Budget, Approaching Limit, Over Budget).

---

## 4. Code Structure & Architecture Guidelines
Structure your repository cleanly into separate modules/layers:
- **`database.py`**: Handles database connection, table creation, and all CRUD (Create, Read, Update, Delete) query functions.
- **`app.py`**: Handles Streamlit UI layouts, user interactions, and calls to database functions.
- **`visualizations.py`** *(optional)*: Handles charting and summary calculations.
- **`requirements.txt`**: Complete list of Python dependencies.
- **`README.md`**: Project setup instructions, screenshots, and usage guide.

---

## 5. Non-Functional Requirements
1. **Input Validation**: Ensure robust error handling for invalid inputs, missing fields, and type mismatches.
2. **Database Integrity**: Ensure database connections and cursors are properly opened, committed, and closed to prevent locked database errors.
3. **UI/UX Consistency**: Maintain clean layout structuring (use Streamlit columns, tabs, metrics, and sidebars effectively).

---

## 6. Deliverables & Submission
Submit a zipped repository or a GitHub link containing:
1. All source `.py` files.
2. `requirements.txt`.
3. `README.md` with instructions on how to install dependencies and run the Streamlit application.
4. Short screen recording or screenshots demonstrating all CRUD operations and analytics charts.

---

## 7. Evaluation Rubric

| Criteria | Description | Weight |
| :--- | :--- | :--- |
| **Database Design & CRUD Operations** | Correct SQLite schema, proper SQL query implementation for Insert, Read, Update, and Delete. | 25% |
| **Streamlit UI & Form Handling** | Responsive forms, clear layout, proper validation, user feedback messages. | 20% |
| **Filtering & Search Functionality** | Accurate multi-condition filtering (date ranges, categories, search terms). | 15% |
| **Data Analytics & Visualizations** | Accurate summary metrics and clear graphical representation of spending habits. | 20% |
| **Code Organization & Cleanliness** | Separation of concerns (UI vs DB logic), naming conventions, docstrings, modularity. | 10% |
| **Documentation & Setup** | Comprehensive `README.md` and complete `requirements.txt`. | 10% |
