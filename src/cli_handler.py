class CLIHandler:
    def __init__(self, intent_recogniser):
        self.intent_recogniser = intent_recogniser

    def get_user_input(self):
        return input("\nYour query: ")

    def display_extracted_info(self, named_entities, intent, details):
        print(f"\nIdentified Named Entities: {named_entities}")
        print(f"Identified Intent: {intent}")
        print(f"Details (Genres): {details}")

    def run(self):
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
