"""
Lightweight translation service with optional neural model.


By default, runs in a safe fallback mode that returns the original text so the
backend starts quickly without heavyweight dependencies. If transformers + torch
are installed and the model is available, it will use IndicTrans2.
"""

# Optional neural dependencies (heavy). Wrapped to avoid import-time crashes.
try:
    from transformers import AutoModelForSeq2SeqLM, AutoTokenizer  # type: ignore
    import torch  # type: ignore
    _NEURAL_DEPS_AVAILABLE = True
except Exception:
    AutoModelForSeq2SeqLM = None  # type: ignore
    AutoTokenizer = None  # type: ignore
    torch = None  # type: ignore
    _NEURAL_DEPS_AVAILABLE = False

class TranslationService:
    def __init__(self):
        # Mode: "neural" if deps available, else "fallback"
        self.mode = "neural" if _NEURAL_DEPS_AVAILABLE else "fallback"

        self.model_name = "ai4bharat/indictrans2-en-indic-1B"
        self.tokenizer = None
        self.model = None
        self.device = "cpu"

        if self.mode == "neural":
            try:
                self.tokenizer = AutoTokenizer.from_pretrained(self.model_name, trust_remote_code=True)
                self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name, trust_remote_code=True)
                self.device = "cuda" if torch and torch.cuda.is_available() else "cpu"  # type: ignore[attr-defined]
                self.model.to(self.device)
            except Exception as load_error:
                # Fall back silently to keep server healthy
                print(f"TranslationService: neural model unavailable ({load_error}). Falling back to passthrough mode.")
                self.mode = "fallback"
                self.tokenizer = None
                self.model = None

        # Language codes supported by IndicTrans2
        self.language_map = {
            'en': 'eng_Latn',
            'hi': 'hin_Deva',
            'te': 'tel_Telu',
            'ta': 'tam_Taml',
            'bn': 'ben_Beng'
        }

    def translate(self, text, target_language='hi'):
        """
        Translate text using IndicTrans2 model
        """
        try:
            if target_language not in self.language_map:
                return text

            if self.mode != "neural" or not self.model or not self.tokenizer:
                # Safe passthrough to avoid heavy deps and long startup
                return text

            tgt_lang = self.language_map[target_language]

            inputs = self.tokenizer(
                text,
                return_tensors="pt",
                padding=True,
                truncation=True
            ).to(self.device)

            with torch.no_grad():  # type: ignore[union-attr]
                generated_tokens = self.model.generate(
                    **inputs,
                    forced_bos_token_id=self.tokenizer.lang_code_to_id[tgt_lang]
                )

            translated_text = self.tokenizer.batch_decode(
                generated_tokens,
                skip_special_tokens=True
            )[0]

            return translated_text

        except Exception as e:
            print(f"Translation error: {str(e)}")
            return text

    def get_supported_languages(self):
        return {
            'en': 'English',
            'hi': 'हिंदी (Hindi)',
            'te': 'తెలుగు (Telugu)',
            'ta': 'தமிழ் (Tamil)',
            'bn': 'বাংলা (Bengali)'
        }

    def translate_internship_data(self, internship, target_language):
        if target_language == 'en':
            return internship

        translated_internship = internship.copy()
        fields_to_translate = ['title', 'company', 'description', 'sector']

        for field in fields_to_translate:
            if field in translated_internship:
                translated_internship[field] = self.translate(
                    translated_internship[field],
                    target_language
                )

        if 'requirements' in translated_internship:
            if 'skills' in translated_internship['requirements']:
                translated_internship['requirements']['skills'] = [
                    self.translate(skill, target_language)
                    for skill in translated_internship['requirements']['skills']
                ]

        return translated_internship

    def translate_recommendations(self, recommendations, target_language):
        if target_language == 'en':
            return recommendations

        translated_recommendations = []
        for recommendation in recommendations:
            translated_rec = self.translate_internship_data(recommendation, target_language)

            if 'match_reasons' in translated_rec:
                translated_rec['match_reasons'] = [
                    self.translate(reason, target_language)
                    for reason in translated_rec['match_reasons']
                ]

            translated_recommendations.append(translated_rec)

        return translated_recommendations
