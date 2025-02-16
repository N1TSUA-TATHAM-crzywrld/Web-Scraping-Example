# Web-Scraping-Example
# Sothebys Realty Web Scraper

## 📌 Overview
This is a **web scraper** built using **Python, Selenium, and BeautifulSoup** to extract real estate agent information from the **Sothebys Realty Seattle** website. The scraper navigates through multiple pages, extracts agent details (name, position, company, address, contact information), and saves them in **structured JSON format**.

## 🚀 Features
- **Automated navigation** using Selenium WebDriver.
- **Extracts structured data** (name, position, company, address, contacts).
- **Handles pagination dynamically**.
- **Saves results in properly formatted JSON**.
- **Runs headless** (silent, without opening a browser window).

---

## 📂 Project Structure
```
├── sothebys_scraper.py  # Main script
├── requirements.txt     # Python dependencies
├── README.md            # Documentation
└── output.json          # Extracted data
```

---

## 🛠️ Installation & Setup

### 1️⃣ Install Dependencies
Ensure you have **Python 3.x** installed. Install required packages:
```sh
pip install selenium beautifulsoup4 html5lib
```

### 2️⃣ Download WebDriver
This scraper uses **Microsoft Edge WebDriver**. Download it from:
[https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/)

Place the `msedgedriver.exe` file in the specified directory (or add it to your system PATH).

### 3️⃣ Run the Scraper
Modify the `driver_path` in `sothebys_scraper.py` to point to your **Edge WebDriver**, then run:
```sh
python sothebys_scraper.py
```

---

## 📜 How It Works
The scraper follows these steps:

### 1️⃣ **Initialize WebDriver**
```python
def initialize_webdriver(driver_path):
    service = Service(driver_path)
    options = EdgeOptions()
    options.add_argument("--headless")
    return webdriver.Edge(service=service, options=options)
```
- Loads the **Edge WebDriver**.
- Runs in **headless mode** (does not open a visible browser window).

---

### 2️⃣ **Navigate to Page & Extract HTML**
```python
def navigate_to_page(browser, url):
    browser.get(url)
```
- Opens the **Sothebys Realty agents page**.
- Extracts the **HTML source**.

---

### 3️⃣ **Extract Agent Data**
```python
def extract_data(browser):
    soup = BeautifulSoup(browser.page_source, 'html5lib')
    agents = []
    
    info_IDs = soup.find_all(id=re.compile("Entity_180"))
    for info in info_IDs:
        text = info.text.strip().split("\n")
        
        agent_data = {
            "name": text[0].strip(),
            "position": text[1].strip(),
            "company": text[2].strip(),
            "address": " ".join(text[3:6]).strip()
        }
        
        contact_info = {}
        for line in text:
            if "M:" in line:
                contact_info["CONTACT M"] = line.split("M:")[1].strip()
            if "O:" in line:
                contact_info["CONTACT O"] = line.split("O:")[1].strip()
        
        agent_data.update(contact_info)
        agents.append(agent_data)
    
    with open("output.json", "w", encoding="utf-8") as f:
        json.dump(agents, f, indent=4)
```
#### 🛠️ **Breakdown:**
- **Finds agent sections** in HTML (`Entity_180`).
- **Extracts name, position, company, and address**.
- **Detects contact numbers dynamically**.
- **Formats the data** into a dictionary.
- **Saves to `output.json` in proper JSON format**.

---

### 4️⃣ **Handle Pagination**
```python
def full_extraction(browser, url):
    navigate_to_page(browser, url)
    sleep(2)
    soup = references(browser.page_source)
    links = soup.find_all(href=re.compile("-pg"))
    
    pg_numbers = re.findall(r'\d', str(links))
    end_page = max(map(int, pg_numbers))
    count = list(range(1, end_page + 1))
    
    total_pages = [f"{url}/{x}-pg" for x in count]
    
    for page in total_pages:
        navigate_to_page(browser, page)
        sleep(4)
        extract_data(browser)
```
#### 🔹 **What This Does:**
- Detects **pagination links** (e.g., `?page=2`).
- Extracts the **total number of pages**.
- Iterates through **each page**, extracting agent data.

---

## 🏆 Output Example
After running the script, `output.json` will look like this:
```json
[
    {
        "name": "Jay Alan",
        "position": "BROKER",
        "company": "Realogics Sotheby's International Realty",
        "address": "4031 E. Madison Street Seattle, WA, 98112 United States",
        "CONTACT M": "+1 206.391.9000"
    },
    {
        "name": "George Beasley",
        "position": "BROKER",
        "company": "Realogics Sotheby's International Realty",
        "address": "2715 1st Avenue Seattle, WA, 98121 United States",
        "CONTACT M": "+1 206.617.4758",
        "CONTACT O": "+1 206.538.0730"
    }
]
```

---

## 💡 Future Improvements
- 🔹 Add error handling for network issues.
- 🔹 Implement **multi-threading** for faster scraping.
- 🔹 Convert data into a **CSV export** option.

---

## 📜 License
This project is for educational purposes. Feel free to modify and use it!

---

## ⭐ Contribute
Found a bug? Want to improve the script? Open a pull request!

---

## 📞 Contact
💬 Have questions? Reach out!

📧 **Email:** your.email@example.com  
🐙 **GitHub:** [your-github-profile](https://github.com/your-github-profile)

