from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import yagmail
from selenium.webdriver.chrome.options import Options 

# -----------------------------------
# CONFIGURATION
# -----------------------------------
ACCOUNTS = [
    {"email": "danidesousa2005@gmail.com", "password": "DaniDeSousa95"},
    {"email": "alexandroten5@gmail.com", "password": "DaniDeSousa95"},
]

YOUR_EMAIL = "danidesousa2005@gmail.com"
YOUR_EMAIL_APP_PASSWORD = "dwlsfjwerrtlfzpl"

# -----------------------------------
# LOGIN + ACTIONS POUR CHAQUE COMPTE
# -----------------------------------
def run_for_account(email, password):

    # --- Configuration du WebDriver en mode HEADLESS (obligatoire sur GitHub Actions) ---
    chrome_options = Options()
    # Arguments CRUCIAUX pour Linux CI/CD:
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage") 
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Création du WebDriver avec les options Headless
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), 
        options=chrome_options
    )
    
    driver.get("https://seeuus.com/login")
    wait = WebDriverWait(driver, 20)

    try:
        print(f"\n--- Début du traitement pour {email} ---")

        # --- 1. CONNEXION ---
        mailbox_tab = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[contains(text(), 'Mailbox')]")))
        mailbox_tab.click()
        time.sleep(1)

        email_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='text' and @placeholder='Please enter your email address']")))
        email_input.send_keys(email)
        password_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='password' and @placeholder='Please enter your password']")))
        password_input.send_keys(password)

        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Login')]")))
        login_button.click()
        time.sleep(3) 
        
        sign_in_now_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//div[contains(text(), 'Sign in now') and contains(@class, 'submit')]")
        ))
        sign_in_now_button.click()
        print("-> [OK] Clic sur 'Sign in now' (Validation de la connexion).")
        time.sleep(2)
        
    except Exception as e:
        print(f"-> [ERREUR] Échec de la connexion/Sign-in pour {email} : {e}")
        driver.quit()
        return False

    # ---------------------------
    # RÉCOMPENSE QUOTIDIENNE (WELFARE)
    # ---------------------------
    try:
        driver.get("https://seeuus.com/welfare")
        time.sleep(3)

        # Cherche la case de récompense active en se basant sur le texte 'Sign in'
        sign_in_reward_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//*[contains(text(), 'Sign in')]") 
        ))
        
        sign_in_reward_button.click()
        print("-> [OK] Clic sur le bouton 'Sign in' (Récompense du jour).")
        time.sleep(2)

        # Clic sur "OK" dans le pop-up de confirmation
        ok_btn = wait.until(EC.element_to_be_clickable(
             (By.XPATH, "//div[contains(text(), 'OK') and contains(@class, 'submit')]")
        ))
        ok_btn.click()
        print(f"-> [OK] Récompense prise pour {email}.")
        time.sleep(2)
        
    except Exception as e:
        # L'exception est levée si la récompense est déjà réclamée ou si un élément n'est pas trouvé.
        print(f"-> [INFO] Aucune récompense 'Sign in' disponible ou erreur ({e}).")

    # ---------------------------
    # CRÉER L'ORDER (GRID)
    # ---------------------------
    try:
        driver.get("https://seeuus.com/grid")
        time.sleep(3) 

        # Create Order
        create_order_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(text(), 'Create order') and contains(@class, 'buts1')]")
        ))
        create_order_btn.click()
        time.sleep(1)

        # ALL
        all_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//div[contains(text(), 'All') and contains(@class, 'all')]")
        ))
        all_btn.click()
        time.sleep(1)

        # Start AI
        start_ai_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//div[contains(text(), 'Start AI') and contains(@class, 'submit')]")
        ))
        start_ai_btn.click()
        print(f"-> [OK] Ordre créé et 'Start AI' lancé pour {email}.")
        time.sleep(3)

    except Exception as e:
        print(f"-> [ERREUR] Erreur lors de la création de l'ordre pour {email} : {e}")
        driver.quit()
        return False

    driver.quit()
    return True


# -----------------------------------
# ENVOI EMAIL
# -----------------------------------
def send_confirmation():
    try:
        yag = yagmail.SMTP(YOUR_EMAIL, YOUR_EMAIL_APP_PASSWORD)
        yag.send(
            to=YOUR_EMAIL,
            subject="SEEUS – Script terminé",
            contents="Les tâches ont été effectuées avec succès sur les comptes configurés."
        )
        print("\n✅ Email de confirmation envoyé.")
    except Exception as e:
        print(f"\n❌ Erreur lors de l'envoi de l'email : Vérifiez le mot de passe d'application. Erreur: {e}")

# -----------------------------------
# MAIN
# -----------------------------------
if __name__ == "__main__":
    success_count = 0
    total_accounts = len(ACCOUNTS)
    
    for acc in ACCOUNTS:
        if run_for_account(acc["email"], acc["password"]):
            success_count += 1

    if success_count > 0:
        print(f"\nRésumé : {success_count}/{total_accounts} comptes traités avec succès.")
        send_confirmation()
    else:
        print("\nRésumé : Échec de toutes les tâches. Aucun email de confirmation envoyé.")