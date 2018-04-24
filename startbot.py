import os
import time
import re
from slackclient import SlackClient
import os
import time
import re
from slackclient import SlackClient
import librarybot

SLACK_BOT_TOKEN = ''
with open('bot_secret_token', 'r', encoding='utf-8') as file:
    SLACK_BOT_TOKEN = file.readline()



# instantiate Slack client
slack_client = SlackClient(SLACK_BOT_TOKEN)
# starterbot's user ID in Slack: value is assigned after the bot starts up
starterbot_id = None

# constants
RTM_READ_DELAY = 1  # 1 second delay between reading from RTM
EXAMPLE_COMMAND = "do"
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"


def parse_bot_commands(slack_events):
    """
        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
    """
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_direct_mention(event["text"])
            if user_id == starterbot_id:
                return message, event["channel"]
    return None, None


def parse_direct_mention(message_text):
    """
        Finds a direct mention (a mention that is at the beginning) in message text
        and returns the user ID which was mentioned. If there is no direct mention, returns None
    """
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)


def generate_response(msg):
    # TODO: Implement more commands
    response = ''
    if command.lower().strip().startswith('help'):
        response = 'Here is what I can do:\n'
        response += 'list books\n'
        response += 'list books for <class abbreviation> <class number>'
    elif command.lower().strip().startswith('list books for'):
        class_name = command[command.lower().find('for') + len('for'):]
        for row in librarybot.get_record_by_attribute('Class', class_name):
            response += str(row['Book']) + '\n'
        if not response:
            response = 'No books found for {}'.format(class_name.strip())
    elif command.lower().strip().startswith('list books'):
        for row in librarybot.get_all_records():
            response += str(row['Book']) + '\n'
    else:
        response = None
    return response


def handle_command(command, channel):
    """
        Executes bot command if the command is known
    """
    # Default response is help text for the user
    default_response = "Not sure what you mean. Type \'help\' for a list of commands."

    # Finds and executes the given command, filling in response
    response = generate_response(command)

    # Sends the response back to the channel
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response or default_response
    )
    print('command completed')


if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            command, channel = parse_bot_commands(slack_client.rtm_read())
            if command:
                handle_command(command, channel)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")
