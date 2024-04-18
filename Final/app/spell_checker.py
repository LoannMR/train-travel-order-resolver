import language_tool_python

def spell_check(sentence):
    """
    Correct spelling mistakes in the sentence as long as they occur
    """
    # Initialize LanguageToolPublicAPI
    with language_tool_python.LanguageToolPublicAPI('fr') as tool:
        # Initialize the corrected version
        corrected_old = sentence
        corrected_new = tool.correct(corrected_old)

        # Perform spell checking until no more corrections are made
        while corrected_new != corrected_old and corrected_new:
            corrected_old = corrected_new
            corrected_new = tool.correct(corrected_old)

    
    return corrected_new