import time
import logging
import threading
import numpy as np  # Importing NumPy library
from scripts.automation.engine_template import (
    AutomationEngine,
    example_task,
    exploitation_task,
    lateral_movement_task,
    exfiltration_task
)
from scripts.learning.learning_module import LearningModule
from scripts.update_manager import UpdateManager
from scripts.reporting_system import ReportingSystem
from scripts.picoctf_interaction import (
    PicoCTFInteraction
)  # Importing PicoCTF interaction module
from scripts.nlu_pipeline import (
    tokenize,
    named_entity_recognition,
    classify_intent
)  # Importing NLU pipeline functions

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='/home/ubuntu/VishwamAI/logs/agent.log'
)


class RedTeamAgent:
    def __init__(self):
        self.running = True
        self.reporting_system = ReportingSystem()
        self.automation_engine = AutomationEngine(self.reporting_system)
        self.learning_module = LearningModule()
        self.update_manager = UpdateManager()
        self.picoctf_interaction = PicoCTFInteraction()  # Initializing PicoCTF
        self.initialize_tasks()
        self.reporting_system.log_activity("RedTeamAgent initialized.")

    def initialize_tasks(self):
        # Replace the example targets with actual targets relevant to red team
        # operations
        self.automation_engine.add_task(
            example_task, "127.0.0.1"
        )  # Example target, replace with actual target
        self.automation_engine.add_task(
            exploitation_task, "127.0.0.1"
        )  # Example target, replace with actual target
        self.automation_engine.add_task(
            lateral_movement_task, "127.0.0.1"
        )  # Example target, replace with actual target
        self.automation_engine.add_task(
            exfiltration_task, "127.0.0.1"
        )  # Example target, replace with actual target
        self.automation_engine.add_task(
            self.picoctf_interaction.solve_challenge, "example_challenge_id"
        )  # Example challenge, replace with actual challenge ID

    def start(self):
        self.update_thread = threading.Thread(target=self.update_manager.run)
        self.update_thread.start()
        self.reporting_system.log_activity("RedTeamAgent started.")
        iteration_count = 0
        max_iterations = 10  # Set a maximum number of iterations for testing
        while self.running:
            logging.info(
                f"Loop iteration {iteration_count} - self.running: "
                f"{self.running}"
            )
            if iteration_count >= max_iterations:
                logging.info(
                    "Reached maximum iterations, setting running flag to "
                    "False."
                )
                self.running = False
            if not self.running:
                logging.info("Running flag is False, exiting loop.")
                break
            self.run_tasks()
            # Sleep for a short duration to simulate continuous operation
            time.sleep(1)
            iteration_count += 1
            logging.info(
                f"Iteration {iteration_count} completed - self.running: "
                f"{self.running}"
            )
        logging.info(
            f"Loop has exited - self.running: {self.running}, "
            f"iteration_count: {iteration_count}"
        )
        self.stop()  # Ensure the stop method is called after the loop exits

    def run_tasks(self):
        logging.info("Running automated tasks...")
        self.reporting_system.log_activity("Running automated tasks...")
        try:
            logging.info("Starting task execution in automation engine.")
            self.automation_engine.run_tasks()
            logging.info("Task execution completed in automation engine.")
            # Example of using the learning module with dummy data
            raw_data = self.collect_data()
            if raw_data is not None:
                logging.info(
                    "Starting incremental training with collected data."
                )
                self.learning_module.incremental_train(raw_data)
                logging.info("Incremental training completed.")
        except Exception as e:
            logging.error(f"Error running tasks: {e}")
            self.reporting_system.log_activity(
                f"Error running tasks: {e}"
            )

    def collect_data(self):
        # Placeholder for data collection logic
        # Replace with actual data collection from red team operations
        collected_data = []
        for task_function, args, kwargs in self.automation_engine.tasks:
            try:
                result = task_function(*args, **kwargs)
                if result is None:
                    logging.info(
                        f"Task {task_function.__name__} returned None, "
                        "skipping."
                    )
                    continue
                if isinstance(result, dict):
                    logging.info(
                        f"Task {task_function.__name__} returned a "
                        "dictionary, skipping shape check."
                    )
                    continue
                if isinstance(result, np.ndarray) and result.ndim == 1:
                    result = result.reshape(1, -1)  # Ensure result is 2D
                logging.info(
                    f"Task {task_function.__name__} returned result with "
                    f"shape: {result.shape}"
                )
                # Validate dimensions before appending
                # Validate dimensions before appending
                if collected_data and result.shape[1] != collected_data[0].shape[1]:
                    logging.error(
                        f"incompatible dimensions: {result.shape}"
                    )
                    self.reporting_system.log_activity(
                        f"Task {task_function.__name__} returned result with "
                        f"incompatible dimensions: {result.shape}"
                    )
                    continue
                collected_data.append(result)
            except Exception as e:
                logging.error(
                    f"Error collecting data from task "
                    f"{task_function.__name__}: {e}"
                )
                self.reporting_system.log_activity(
                    f"Error collecting data from task "
                    f"{task_function.__name__}: {e}"
                )
        if collected_data:
            if all(data.shape[1] == 0 for data in collected_data):
                logging.error("Collected data has no features.")
                self.reporting_system.log_activity(
                    "Collected data has no features."
                )
                return None
            # Stack collected data into a 2D array
            return np.vstack(collected_data)
        return None

    def process_natural_language_input(self, input_text):
        """
        Process natural language input using the NLU pipeline and determine
        actions.
        """
        try:
            # Tokenize the input text
            tokens = tokenize(input_text)
            logging.info(f"Tokens: {tokens}")

            # Perform Named Entity Recognition (NER)
            entities = named_entity_recognition(input_text)
            logging.info(f"Entities: {entities}")

            # Define candidate labels for intent classification
            candidate_labels = [
                "reconnaissance", "exploitation", "lateral movement",
                "exfiltration", "reporting"
            ]

            # Classify the intent of the input text
            intent = classify_intent(input_text, candidate_labels)
            logging.info(f"Intent: {intent}")

            # Mapping of intents to task functions and parameters
            intent_task_mapping = {
                "reconnaissance": (example_task, "127.0.0.1"),
                "exploitation": (exploitation_task, "127.0.0.1"),
                "lateral movement": (lateral_movement_task, "127.0.0.1"),
                "exfiltration": (exfiltration_task, "127.0.0.1"),
                "reporting": (self.reporting_system.generate_report,)
            }

            # Determine actions based on the classified intent
            top_intent = intent['labels'][0]
            if top_intent in intent_task_mapping:
                task_function, *task_args = intent_task_mapping[top_intent]
                self.automation_engine.add_task(task_function, *task_args)
            else:
                logging.warning(f"Unrecognized intent: {top_intent}")

        except Exception as e:
            logging.error(
                f"Error processing natural language input: {e}"
            )
            self.reporting_system.log_activity(
                f"Error processing natural language input: {e}"
            )

    def list_challenges(self):
        try:
            challenges = self.picoctf_interaction.list_challenges()
            logging.info(f"Available challenges: {challenges}")
            self.reporting_system.log_activity(
                f"Available challenges: {challenges}"
            )
        except Exception as e:
            logging.error(f"Error listing challenges: {e}")
            self.reporting_system.log_activity(
                f"Error listing challenges: {e}"
            )

    def stop(self):
        logging.info("Stop method called. Setting running flag to False.")
        self.running = False
        self.update_manager.running = False
        logging.info(
            "Running flag set to False. Attempting to join update thread."
        )
        try:
            self.update_thread.join(timeout=5)  # Add a timeout to the join
            if self.update_thread.is_alive():
                logging.error(
                    "Update thread did not terminate within the timeout "
                    "period."
                )
            else:
                logging.info("Update thread joined successfully.")
        except Exception as e:
            logging.error(f"Error joining update thread: {e}")
        logging.info(
            f"Stop method completed - self.running: {self.running}, "
            f"update_manager.running: {self.update_manager.running}"
        )
        self.learning_module.save_model("trained_model.pkl")
        self.reporting_system.log_activity("Agent stopped and model saved.")
        logging.info("Agent stopped and model saved.")
        report_file = self.reporting_system.generate_report()
        logging.info(
            f"Report generated: {report_file}"
        )


if __name__ == "__main__":
    agent = RedTeamAgent()
    try:
        agent.start()
    except KeyboardInterrupt:
        agent.stop()
        logging.info("Agent stopped by user.")

# TODO: Replace the example targets with actual targets relevant to red team
# operations.
# TODO: Update the data collection logic with actual data collection from red
# team operations.
# TODO: Implement security measures to ensure the agent operates safely and
# securely.
