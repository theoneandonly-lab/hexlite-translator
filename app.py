import streamlit as st

class HexLiteTranslator:
    def __init__(self):
        self.groups = ["ABCDEFGHI", "JKLMNOPQR", "STUVWXYZ"]
        self.alphabet = "".join(self.groups)
        self.total_chars = len(self.alphabet)

    def encode(self, text, shift=0):
        words = text.upper().split(" ")
        encoded_words = []
        for word in words:
            encoded_chars = []
            for char in word:
                if char in self.alphabet:
                    orig_pos = self.alphabet.index(char)
                    new_pos = (orig_pos + shift) % self.total_chars
                    g_idx = (new_pos // 9) + 1
                    p_idx = (new_pos % 9) + 1
                    encoded_chars.append(f"{g_idx}{p_idx}")
                else:
                    encoded_chars.append(char)
            encoded_words.append(".".join(encoded_chars))
        return "/ ".join(encoded_words)

    def decode(self, text, shift=0):
        encoded_words = text.split("/ ")
        decoded_words = []
        for encoded_word in encoded_words:
            tokens = encoded_word.split(".")
            decoded_chars = []
            for token in tokens:
                if len(token) == 2 and token.isdigit():
                    g_idx = int(token[0]) - 1
                    p_idx = int(token[1]) - 1
                    flat_pos = (g_idx * 9) + p_idx
                    orig_pos = (flat_pos - shift) % self.total_chars
                    decoded_chars.append(self.alphabet[orig_pos])
                else:
                    decoded_chars.append(token)
            decoded_words.append("".join(decoded_chars))
        return " ".join(decoded_words)

# --- Graphical Website Interface Configuration ---
translator = HexLiteTranslator()

st.title("HexLite Secret Cipher Portal")
st.write("Convert your custom coordinates and text instantly.")

# Interactive dropdowns and configuration options
mode = st.selectbox("Choose Mode", ["Encode (Text to Code)", "Decode (Code to Text)"])
shift = st.number_input("Shift Key Number", min_value=0, value=0, step=1)
message = st.text_area("Enter your message here")

if st.button("Process Message"):
    if message.strip() == "":
        st.warning("Please type a message first.")
    else:
        if "Encode" in mode:
            result = translator.encode(message, shift)
            st.success("Your Encoded Result:")
        else:
            result = translator.decode(message, shift)
            st.success("Your Decoded Result:")
        
        # Displays the result inside a clean copy-paste container box
        st.code(result)
