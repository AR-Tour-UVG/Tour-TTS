from google.cloud import texttospeech
import html

def text_to_ssml(inputfile: str) -> str:
    """
    Generates SSML text from plaintext.
    Given an input filename, this function converts the contents of the text
    file into a string of formatted SSML text. This function formats the SSML
    string so that, when synthesized, the synthetic audio will pause for two
    seconds between each line of the text file. This function also handles
    special text characters which might interfere with SSML commands.

    Args:
        inputfile: name of plaintext file
    Returns: SSML text based on plaintext input
    """

    # Parses lines of input file
    with open(inputfile) as f:
        raw_lines = f.read()

    # Replace special characters with HTML Ampersand Character Codes
    # These Codes prevent the API from confusing text with
    # SSML commands
    # For example, '<' --> '&lt;' and '&' --> '&amp;'

    escaped_lines = html.escape(raw_lines)

    # Convert plaintext to SSML
    # Wait two seconds between each address
    ssml = "<speak>{}</speak>".format(
        escaped_lines.replace("\n", '\n<break time="2s"/>')
    )

    # Return the concatenated string of ssml script
    return ssml


def ssml_to_audio(ssml_text: str, output: str) -> None:
    """
    Generates SSML text from plaintext.
    Given a string of SSML text and an output file name, this function
    calls the Text-to-Speech API. The API returns a synthetic audio
    version of the text, formatted according to the SSML commands. This
    function saves the synthetic audio to the designated output file.

    Args:
        ssml_text: string of SSML text
    """

    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Sets the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(ssml=ssml_text)

    # Builds the voice request, selects the language code ("en-US") and
    # the SSML voice gender ("MALE")
    voice = texttospeech.VoiceSelectionParams(
        language_code="es-US", name="es-US-Polyglot-1", ssml_gender=texttospeech.SsmlVoiceGender.MALE 
    )

    # Selects the type of audio file to return
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Performs the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # Writes the synthetic audio to the output file.
    with open(output, "wb") as out:
        out.write(response.audio_content)
        print(f"Audio content written to file {output}" )

if __name__ == "__main__":

    welcome_msg = """
    <speak>
        Hola, Soy Jack, y seré tu guía virtual. 
        <break time="500ms"/>
        Te doy la bienvenida al Tour de Realidad Aumentada por la <say-as interpret-as="characters">UBG</say-as>
        <break time="600ms"/>
        ¡Vamos!
    </speak>
    """

    tour_startup = """
    <speak>
        Ahora, para comenzar, presiona el botón con el ícono de brújula en la esquina superior izquierda. 
        <break time="500ms"/>
        Luego elige uno de los tours disponibles y toca comenzar.
    </speak>
    """

    tour_guide = """
    <speak>
        ¡Comenzamos el tour!  
        <break time="400ms"/> 
        Este es un recorrido de prueba para que conozcas cómo funciona la app.
        <break time="500ms"/>
        Durante el recorrido, sigue la flecha y acércate a los sensores morados.
    </speak>
    """

    follow_arrow = """
    <speak>
    Sigue la flecha.
    </speak>
    """

    stop_info = """
    <speak>
    Has llegado a una parada.
    <break time="400ms"/>
    Aquí podrás ver información importante sobre este lugar.
    </speak>
    """

    first_stop = """
    <speak>
    Has llegado a la primera parada.
    </speak>
    """

    continue_tour = """
    <speak>
    Cuando estés listo, presiona siguiente y sigue la flecha al siguiente punto.
    </speak>
    """

    tour_end = """
    <speak>
    ¡Felicidades! Has completado el tour.
    </speak>
    """

    # Generate SSML text from plaintext
    ssml_to_audio(welcome_msg, "test-audio/welcome_msg.mp3")
    ssml_to_audio(tour_startup, "test-audio/tour_startup.mp3")
    ssml_to_audio(tour_guide, "test-audio/tour_guide.mp3")
    ssml_to_audio(follow_arrow, "test-audio/follow_arrow.mp3")
    ssml_to_audio(stop_info, "test-audio/stop_info.mp3")
    ssml_to_audio(continue_tour, "test-audio/continue_tour.mp3")
    ssml_to_audio(tour_end, "test-audio/tour_end.mp3")
    ssml_to_audio(first_stop, "test-audio/first_stop.mp3")
    print("All audio files generated successfully.")