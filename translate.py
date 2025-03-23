import os
import re
import json
from bs4 import BeautifulSoup
import translators as ts
import time
from tqdm import tqdm

# Translation cache
CACHE_FILE = 'translation_cache.json'
translation_cache = {}

def load_cache():
    """Load translation cache from file"""
    global translation_cache
    try:
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                translation_cache = json.load(f)
            print(f"Loaded {len(translation_cache)} cached translations")
    except Exception as e:
        print(f"Error loading cache: {e}")

def save_cache():
    """Save translation cache to file"""
    try:
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(translation_cache, f, ensure_ascii=False, indent=2)
        print(f"Saved {len(translation_cache)} translations to cache")
    except Exception as e:
        print(f"Error saving cache: {e}")

def get_dutch_translations():
    """Get dictionary of Dutch to English translations"""
    translations = {
        # Menu items and titles
        "Inleiding": "Introduction",
        "Model": "Model",
        "Overzicht rechtsvormen": "Overview of Legal Forms",
        "HR Model Overzicht (conceptueel)": "Trade Register Model Overview (conceptual)",
        "HR Model Overzicht (volledig)": "Trade Register Model Overview (complete)",
        "HR Model Objecttypen": "Trade Register Model Object Types",
        "HR Model Gegevensgroepen": "Trade Register Model Data Groups",
        "HR Model Domeinwaarden": "Trade Register Model Domain Values",
        "Referenties": "References",
        "Inhoud van het handelsregister": "Contents of the Trade Register",
        "inhoud van het handelsregister": "Contents of the Trade Register",
        "Content of the trade register": "Contents of the Trade Register",
        "Content of the Trade Register": "Contents of the Trade Register",
        "Identificerende gegevens": "Identifying Data",
        "Handelsregister": "Trade Register",
        "Beschrijving": "Description",
        "Toelichting": "Explanation",
        "Gegevensgroep": "Data Group",
        "Wetgeving": "Legislation",
        "Documentatie": "Documentation",
        "Kamer van Koophandel": "Chamber of Commerce",
        "Basisregistraties": "Basic Registrations",
        "Openbare gegevens": "Public Data",
        "Niet-openbare gegevens": "Non-public Data",
        "Advocaten": "Lawyers",
        "Notarissen": "Notaries",
        "Deurwaarders": "Bailiffs",
        "Beschermde adressen": "Protected Addresses",
        "Handelsregister Dataservice": "Trade Register Data Service",
        "Databankrechten": "Database Rights",
        "Openbaar": "Public",
        "Niet-openbaar": "Non-public",
        "Autorisatieniveaus": "Authorization Levels",
        "Markt": "Market",
        "Datacatalogus": "Data Catalog",
        "Datacatalogus 3.0.4h": "Data Catalog 3.0.4h",
        "Data catalog 3. 0. 4h": "Data Catalog 3.0.4h",
        "Data Catalog 3. 0. 4h": "Data Catalog 3.0.4h",
        "Data catalog": "Data Catalog",
        "Overzicht": "Overview",
        "Rechtsvormen": "Legal Forms",
        "Objecttypen": "Object Types",
        "Gegevensgroepen": "Data Groups",
        "Domeinwaarden": "Domain Values",
        "Buitenlandse onderneming": "Foreign Company",
        "Eenmanszaak": "Sole Proprietorship",
        "Rechtspersoon": "Legal Entity",
        "Samenwerkingsverband": "Partnership",
        "Vestiging": "Establishment",
        "Functionaris": "Official",
        "Gemachtigde": "Authorized Representative",
        "Aansprakelijke": "Liable Party",
        "Eigenaar": "Owner",
        "Bestuurder": "Director",
        "Commissaris": "Commissioner",
        
        # Model overview variations
        "HR-Model Overzicht (conceptueel)": "Trade Register Model Overview (conceptual)",
        "HR Model Overzicht (conceptueel)": "Trade Register Model Overview (conceptual)",
        "HR-Model Overzicht(conceptueel)": "Trade Register Model Overview (conceptual)",
        "HR Model Overzicht(conceptueel)": "Trade Register Model Overview (conceptual)",
        "HR-Model Overzicht - conceptueel": "Trade Register Model Overview - conceptual",
        "HR Model Overzicht - conceptueel": "Trade Register Model Overview - conceptual",
        "HR-Model Overzicht conceptueel": "Trade Register Model Overview (conceptual)",
        "HR Model Overzicht conceptueel": "Trade Register Model Overview (conceptual)",
        "HR-Model Overview (conceptueel)": "Trade Register Model Overview (conceptual)",
        "HR Model Overview (conceptueel)": "Trade Register Model Overview (conceptual)",
        "HR-Model Overview(conceptueel)": "Trade Register Model Overview (conceptual)",
        "HR Model Overview(conceptueel)": "Trade Register Model Overview (conceptual)",
        "HR-Model Overview - conceptueel": "Trade Register Model Overview - conceptual",
        "HR Model Overview - conceptueel": "Trade Register Model Overview - conceptual",
        "HR-Model Overview conceptueel": "Trade Register Model Overview (conceptual)",
        "HR Model Overview conceptueel": "Trade Register Model Overview (conceptual)",
        "HR Model Overview (conceptual)": "Trade Register Model Overview (conceptual)",
        "HR-Model Overview (conceptual)": "Trade Register Model Overview (conceptual)",
        "HR Model Overzicht (volledig)": "Trade Register Model Overview (complete)",
        "HR-Model Overzicht (volledig)": "Trade Register Model Overview (complete)",
        "HR Model Overview (volledig)": "Trade Register Model Overview (complete)",
        "HR-Model Overview (volledig)": "Trade Register Model Overview (complete)",
        "HR Model Overview (full)": "Trade Register Model Overview (complete)",
        "HR-Model Overview (full)": "Trade Register Model Overview (complete)",
        "Hr model overview (conceptual)": "Trade Register Model Overview (conceptual)",
        "hr model overview (conceptual)": "Trade Register Model Overview (conceptual)",
        "hr-model overview (conceptual)": "Trade Register Model Overview (conceptual)",
        "hr-model overview (conceptueel)": "Trade Register Model Overview (conceptual)",
        "hr model overzicht (conceptueel)": "Trade Register Model Overview (conceptual)",
        "hr-model overzicht (conceptueel)": "Trade Register Model Overview (conceptual)",
        "hr model overview (conceptueel)": "Trade Register Model Overview (conceptual)",
        "hr-model overview (conceptueel)": "Trade Register Model Overview (conceptual)",
        "hr model overzicht (conceptual)": "Trade Register Model Overview (conceptual)",
        "hr-model overzicht (conceptual)": "Trade Register Model Overview (conceptual)",
        "hr model overview (conceptual): class diagram": "Trade Register Model Overview (conceptual): class diagram",
        "hr-model overview (conceptual): class diagram": "Trade Register Model Overview (conceptual): class diagram",
        "hr model overzicht (conceptueel): class diagram": "Trade Register Model Overview (conceptual): class diagram",
        "hr-model overzicht (conceptueel): class diagram": "Trade Register Model Overview (conceptual): class diagram",
        "HR model overview (conceptual): class diagram": "Trade Register Model Overview (conceptual): class diagram",
        "HR-model overview (conceptual): class diagram": "Trade Register Model Overview (conceptual): class diagram",
        "HR model overzicht (conceptueel): class diagram": "Trade Register Model Overview (conceptual): class diagram",
        "HR-model overzicht (conceptueel): class diagram": "Trade Register Model Overview (conceptual): class diagram",
        
        # Common words and phrases
        "producten bestellen": "order products",
        "gegevenscatalogus": "data catalog",
        "bevoegde gebruikers": "authorized users",
        "niet-bevoegde gebruikers": "unauthorized users",
        "onder constructie": "under construction",
        "in bewerking": "in progress",
        "raadplegen": "consult",
        "opvragen": "request",
        "inzien": "view",
        "uittreksels": "extracts",
        "producten": "products",
        "diensten": "services",
        
        # Special characters and formatting
        "«": "«",
        "»": "»",
        "<br/>": "<br/>",
    }
    return translations

def clean_html_text(text):
    """Clean and normalize HTML text content"""
    if not text or not isinstance(text, str):
        return text
    
    # Remove multiple spaces
    text = re.sub(r'\s+', ' ', text)
    
    # Fix sentence capitalization
    sentences = re.split(r'([.!?]+)', text)
    for i in range(0, len(sentences), 2):
        if sentences[i].strip():
            sentences[i] = sentences[i].strip().capitalize()
    text = ''.join(sentences)
    
    # Fix common formatting issues
    text = re.sub(r'\s+([.,;:!?])', r'\1', text)  # Remove space before punctuation
    text = re.sub(r'([.,;:!?])([^\s])', r'\1 \2', text)  # Add space after punctuation
    text = re.sub(r'\s+\)', ')', text)  # Fix closing parenthesis
    text = re.sub(r'\(\s+', '(', text)  # Fix opening parenthesis
    
    # Fix specific phrases
    text = text.replace('sacrifices this data', 'provides this data')
    text = text.replace('leg implemented', 'been implemented')
    
    return text.strip()

def should_skip_translation(text):
    """Check if text should be skipped from translation"""
    # Skip empty strings
    if not text or not text.strip():
        return True
        
    # Skip if already in English (more than 50% of words are English)
    words = text.lower().split()
    if words:
        english_words = sum(1 for word in words if not any(c in word for c in 'éëïöüàèìòùâêîôûäëïöü'))
        if english_words / len(words) > 0.5:
            return True
    
    # Skip dates (matches common date formats)
    if re.match(r'^\d{1,2}[-/.]\d{1,2}[-/.]\d{2,4}', text):
        return True
    if re.match(r'^\d{2,4}[-/.]\d{1,2}[-/.]\d{1,2}', text):
        return True
        
    # Skip codes and technical strings
    if re.match(r'^code:?\s*[\'"]?\d+[\'"]?$', text.lower().strip()):
        return True
    # Skip GUIDs and technical identifiers (both with and without curly braces)
    if re.match(r'[{]?[0-9a-f]{8}[-]?([0-9a-f]{4}[-]?){3}[0-9a-f]{12}[}]?', text.lower()):
        return True
    # Skip any text that looks like a technical identifier (alphanumeric with dashes)
    if re.match(r'^[{]?[0-9a-f-]+[}]?$', text.lower()):
        return True
    if '<br/>' in text and len(text.replace('<br/>', '').strip()) < 3:
        return True
    # Skip single words that are likely technical identifiers
    if len(text.split()) == 1 and (text.isupper() or text.islower()) and len(text) <= 4:
        return True
    # Skip any string that's just a number or code with optional quotes
    if re.match(r'^[\'"]?\d+[\'"]?$', text.strip()):
        return True
        
    return False

def translate_text(text, from_lang='nl', to_lang='en', retry_delay=10, max_retries=3):
    """Translate a single text with retries and caching"""
    if should_skip_translation(text):
        return text
        
    # Clean and normalize the text
    text = clean_html_text(text)
    
    # Check translation cache first
    cache_key = text.strip().lower()
    if cache_key in translation_cache:
        return translation_cache[cache_key]
    
    # Check predefined translations
    translations = get_dutch_translations()
    if text in translations:
        return clean_html_text(translations[text])
    
    for attempt in range(max_retries):
        try:
            print(f"Translating: {text[:100]}...")    
            translated = ts.translate_text(text, from_language=from_lang, to_language=to_lang, translator='bing')
            translated = clean_html_text(translated)
            print(f"Translated to: {translated[:100]}...")
            
            # Cache successful translation
            translation_cache[cache_key] = translated
            if len(translation_cache) % 10 == 0:  # Save cache periodically
                save_cache()
                
            time.sleep(2)  # Wait between translations
            return translated
            
        except Exception as e:
            if "429" in str(e) or "Too Many Requests" in str(e):
                print(f"Rate limit hit, waiting {retry_delay} seconds...")
                time.sleep(retry_delay)
                retry_delay *= 2
            else:
                print(f"Translation error: {e}")
                if attempt == max_retries - 1:
                    return text
                time.sleep(retry_delay)
    return text

def translate_xml_files():
    """Translate all XML files in js/data directory"""
    xml_dir = os.path.join("js", "data")
    xml_files = []
    
    # Get all XML files (excluding guidmaps)
    for root, _, files in os.walk(xml_dir):
        if "guidmaps" not in root:  # Skip guidmaps directory
            for file in files:
                if file.endswith(".xml"):
                    xml_files.append(os.path.join(root, file))
    
    print(f"\nTranslating {len(xml_files)} XML files...")
    for xml_file in tqdm(xml_files, desc="Translating files"):
        try:
            with open(xml_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse XML-like content (it's actually JavaScript)
            lines = content.split('\n')
            new_lines = []
            for line in lines:
                if 'new Array(' in line:
                    # Extract the text part (3rd element in array)
                    parts = line.split(',')
                    if len(parts) >= 3:
                        # Get the text part (usually the 3rd element)
                        text_part = parts[2].strip()
                        if text_part.startswith('"') and text_part.endswith('"'):
                            # Extract text between quotes
                            text = text_part[1:-1]
                            # Translate if needed
                            translated = translate_text(text)
                            # Replace original text with translation
                            if translated != text:
                                parts[2] = f'"{translated}"'
                                line = ','.join(parts)
                                print(f"Translated XML item: {text} -> {translated}")
                new_lines.append(line)
            
            # Write back the modified content
            with open(xml_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(new_lines))
                
        except Exception as e:
            print(f"Error processing {xml_file}: {e}")

def translate_html_files():
    """Translate all HTML files in EARoot directory"""
    html_files = []
    
    # Get all HTML files recursively
    for root, _, files in os.walk("EARoot"):
        for file in files:
            if file.endswith(".htm"):
                html_files.append(os.path.join(root, file))
    
    print(f"\nTranslating {len(html_files)} HTML files...")
    for html_file in tqdm(html_files, desc="Translating files"):
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse HTML
            soup = BeautifulSoup(content, 'html.parser')
            
            # Translate title tag
            title_tag = soup.find('title')
            if title_tag and title_tag.string:
                original = title_tag.string.strip()
                translated = translate_text(original)
                if translated != original:
                    title_tag.string.replace_with(translated)
                    print(f"Translated title: {original} -> {translated}")
            
            # Translate ObjectTitle div
            obj_title = soup.find('div', class_='ObjectTitle')
            if obj_title and obj_title.string:
                original = obj_title.string.strip()
                if ': ' in original:  # Handle "title: type" format
                    title_part, type_part = original.split(': ', 1)
                    translated_title = translate_text(title_part)
                    translated = f"{translated_title}: {type_part}"
                else:
                    translated = translate_text(original)
                if translated != original:
                    obj_title.string.replace_with(translated)
                    print(f"Translated object title: {original} -> {translated}")
            
            # Translate other text content
            for elem in soup.find_all(['h1', 'h2', 'h3', 'p', 'div', 'span', 'td', 'th']):
                if elem.get('class') != 'ObjectTitle' and elem.string and elem.string.strip():  # Skip ObjectTitle as it's handled above
                    original = elem.string.strip()
                    translated = translate_text(original)
                    if translated != original:
                        elem.string.replace_with(translated)
                        print(f"Translated HTML: {original} -> {translated}")
            
            # Write back the modified content
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(str(soup))
                
        except Exception as e:
            print(f"Error processing {html_file}: {e}")

def translate_menu_xml():
    """Translate the menu structure XML files"""
    menu_files = ['root.xml']  # Add other menu files if needed
    xml_dir = os.path.join("js", "data")
    
    print("\nTranslating menu structure...")
    for menu_file in menu_files:
        file_path = os.path.join(xml_dir, menu_file)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse XML-like content
            lines = content.split('\n')
            new_lines = []
            for line in lines:
                if 'new Array(' in line:
                    # Extract and translate the title (3rd element)
                    parts = line.split(',')
                    if len(parts) >= 3:
                        text_part = parts[2].strip()
                        if text_part.startswith('"') and text_part.endswith('"'):
                            text = text_part[1:-1]
                            translated = translate_text(text)
                            if translated != text:
                                parts[2] = f'"{translated}"'
                                line = ','.join(parts)
                                print(f"Translated menu item: {text} -> {translated}")
                new_lines.append(line)
            
            # Write back the modified content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(new_lines))
                
        except Exception as e:
            print(f"Error processing menu file {menu_file}: {e}")

def clear_and_rebuild_cache():
    """Clear the translation cache and rebuild it with current rules"""
    global translation_cache
    old_cache = translation_cache.copy()
    translation_cache = {}
    
    print("Clearing and rebuilding translation cache...")
    for dutch_text, english_text in tqdm(old_cache.items(), desc="Processing cache entries"):
        if not should_skip_translation(dutch_text):
            # Re-translate using current rules
            new_translation = translate_text(dutch_text)
            if new_translation != dutch_text:  # Only cache if actually translated
                translation_cache[dutch_text] = new_translation
        else:
            # For skipped items that are identical in both languages, preserve them
            if dutch_text == english_text:
                translation_cache[dutch_text] = english_text
    
    save_cache()
    print(f"Cache rebuilt: {len(translation_cache)} entries")

def main():
    """Main function to run translations"""
    global translation_cache
    
    try:
        load_cache()
        
        # Clear and rebuild cache with new rules
        clear_and_rebuild_cache()
        
        # Translate XML files first (they contain structure)
        translate_xml_files()
        
        # Translate menu structure
        translate_menu_xml()
        
        # Then translate HTML files (they contain content)
        translate_html_files()
        
        # Save final cache
        save_cache()
        
    except Exception as e:
        print(f"Error in main: {e}")

if __name__ == '__main__':
    main()
