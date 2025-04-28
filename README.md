# 🎙️ MoominTranscriber  
*Transcription, romanisation et sous-titrage des épisodes Moomin des années 90*

---

## 🌟 Présentation

**MoominTranscriber** est un outil complet permettant d'extraire, transcrire, romaniser et sous-titrer des épisodes de la série culte *Les Moomins* (version animée des années 1990).  
Ce projet s’inscrit dans une démarche de **préservation culturelle**, d’**accessibilité linguistique** et de **partage poétique** autour d’un univers inoubliable.

---

## 🔧 Fonctionnalités

- 🎞️ **Extraction audio** depuis une vidéo `.mkv`
- ✂️ **Découpage temporel** de l’audio pour des segments spécifiques
- 🧠 **Transcription automatique multilingue** avec [OpenAI Whisper](https://github.com/openai/whisper)
- 🈚 **Romanisation** du japonais (rōmaji)
- 🌍 **Traduction automatique** du finnois vers l'anglais via [Google Translator API](https://pypi.org/project/deep-translator/)
- 🕒 **Génération de sous-titres** au format `.srt` avec gestion des décalages temporels

---

## 📦 Structure du projet

- `extraction_audio.py` → sélection de la vidéo & extraction audio
- `transcribe.py` → découpe de l'audio selon des timestamps
- `romanisation.py` → conversion du texte japonais en rōmaji
- `generate_srt.py` → transformation des transcriptions en fichier `.srt`
- `main.py` → script principal automatisant le processus

---

## ▶️ Utilisation

Lance simplement le script principal :

```bash
python main.py

-- 
Je n'ai pas encore mis les requirements mais ça viendra...
