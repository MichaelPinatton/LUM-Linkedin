import openai
import re
import streamlit as st

openai.api_key == st.secrets["api_key"]

st.title('Web Article ➡️ Linkedin Post')

st.subheader("🛠️ Configuration")

# Sélection du modèle
selected_gpt = st.selectbox(
    'Which OpenAI model?',
    ('gpt-3.5-turbo', 'gpt-4'))

# Sélection de la langue
selected_lang = st.selectbox(
    'Which language for the Linkedin post?',
    ('french', 'english'))

#st.subheader("🪄 Article à transformer")
#url = st.text_area(label='Entrez l\'URL :', value="", height=20)
#submit_button = st.button("Soumettre")

st.subheader("🪄 Article to transform")

title_input = st.text_area(label='Enter the title:', height=100, key="title_input")
submit_button1 = st.button("Submit", key="submit_button1")

text_input = st.text_area(label='Enter the text:', height=500, key="text_input")
submit_button2 = st.button("Submit", key="submit_button2")

linkedin_post_final = ""

if submit_button2:
    text = text_input
    text_len = len(text)
    words = text.split()
    nb_words = len(words)
    
    st.subheader("📖 Original Text")

    st.write(f"Il y a {nb_words} mots et {text_len} caractères")

## Création de parties pour séparation
    sentences = re.split(r'(?<=[.!?])\s+', text)

    part_size = 3000  # Taille maximale de la part en caractères
    parts = []
    current_part = ""

    for sentence in sentences:
        if len(current_part) + len(sentence) <= part_size:
            current_part += sentence
        else:
            parts.append(current_part)
            current_part = sentence

    # Ajouter la dernière part si nécessaire
    if current_part:
        parts.append(current_part)

    nb_parts = len(parts)

    # Afficher le nombre de parties
    parts_dict = {}  # Dictionnaire pour stocker les parties
    st.write("Parts:", nb_parts)
    for i, part in enumerate(parts):
        part_name = f"part_{i+1}"
        parts_dict[part_name] = part
        st.write(f"{part_name}: {parts_dict[part_name]}")

## génération du thread si 1 seule partie

    if nb_parts == 1:
        summaries2 = ''.join(parts)

        prompt_system = f"You are a social media expert specialized in Linkedin. You are known to be very engaging and professional. You will answer in {selected_lang} language only. The Linkedin post you will create is for the company Lumapps, a leading Employee Experience Platform whose goal is to unify the modern workforce through better communication, engagement, and instant access to information."
        prompt_linkedin = f"Create a captivating and informative Linkedin post in less than 130 words from the following article: {title_input}. The post have to include summary from the article {summaries2}. Highlight the key elements of the article. Use a professional and engaging tone. Use sections, small paragraphs and bullet list, so it's easily readable. Use emojis or numbers when appropriate. The hook must be very engaging."

        response = openai.ChatCompletion.create(
        model=selected_gpt,
        messages=[
            {"role": "system", "content": prompt_system},
            {"role": "user", "content": prompt_linkedin},
            ]
        )
        linkedin_post = response.choices[0].message.content.strip()

## génération des résumés pour chaque partie
    if nb_parts != 1:

        summaries = []
        for i, part in enumerate(parts):
            prompt_system = f"You are a content writer specialized in summarizing text in a comprehensive manner. You will answer in {selected_lang} language only."
            prompt_summarize = f"Summarize the following text in less than 100 words for part {i+1}: {part}"
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": prompt_system},
                    {"role": "user", "content": prompt_summarize},
                ]
            )
            summary = response.choices[0].message.content.strip()
            summaries.append(summary)

        # Afficher les résumés
        st.subheader("✍️ Summarize parts")
        for i, summary in enumerate(summaries):
            st.write(f"Summary of part {i+1}: {summary}")

## Génération du Linkedin Thread avec OpenAi

        summaries2 = " ".join(summaries)
        
        prompt_system = f"You are a social media expert specialized in Linkedin. You are known to be very engaging and professional. You will answer in {selected_lang} language only. The Linkedin post you will create is for the company Lumapps, a leading Employee Experience Platform whose goal is to unify the modern workforce through better communication, engagement, and instant access to information."
        prompt_linkedin = f"Create an engaging LinkedIn post in less than 130 words based on the article with the title: {title_input} and the summary: {summaries2}. Write the post in a way that effectively highlights the key points of the article. Use a professional and conversational tone, and adapt the content to the format and style that works best on LinkedIn. Use sections, small paragraphs and bullet list, so it's easily readable. Use emojis or numbers when appropriate. The hook must be very engaging and based on the title."
        response = openai.ChatCompletion.create(
        model = selected_gpt,
        messages=[
            {"role": "system", "content": prompt_system},
            {"role": "user", "content": prompt_linkedin},
            ]
        )
        linkedin_post = response.choices[0].message.content.strip()

    st.subheader("✍️ Linkedin Post :")
    st.markdown(linkedin_post)
