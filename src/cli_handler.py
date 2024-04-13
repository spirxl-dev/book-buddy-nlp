class CLIHandler:
    def __init__(self, intent_recogniser):
        self.intent_recogniser = intent_recogniser

    def get_user_input(self):
        return input("\nYour query: ")

    def display_extracted_info(self, named_entities, intent, details):
        print(f"\n[RESULT] Identified Named Entities: {named_entities}")
        print(f"[RESULT] Identified Intent: {intent}")
        print(f"[RESULT] Output Dictionary: {details}")

    def run(self):
        """ENTRY POINT"""
        print("\nWelcome to Book-Buddy. Please enter your query. ")
        try:
            while True:
                user_input = self.get_user_input()
                named_entities, intent, details = self.intent_recogniser.extract_intent(
                    user_input
                )
                self.display_extracted_info(named_entities, intent, details)
        except KeyboardInterrupt:
            print("\nExiting Book-Buddy...")
