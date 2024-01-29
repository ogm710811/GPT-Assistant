import json
import random


# get recent messages
def get_recent_messages():
    # define the file name and learn instructions
    file_name = "stored_data.json"
    learn_instruction = {
        'role': 'system',
        'content': 'You are a Spanish teacher and your name is Rachel, the user is called Orestes. Keep responses under'
                   ' 20 words. '
    }

    # initialize messages
    messages = []

    # add random elements
    x = random.uniform(0, 1)
    if x < 0.2:
        learn_instruction["content"] = learn_instruction["content"] + "Your response will have some light humour. "
    elif x < 0.5:
        learn_instruction["content"] = learn_instruction["content"] + ("Your response will include an interesting new "
                                                                       "fact about Spain.")
    else:
        learn_instruction["content"] = learn_instruction["content"] + ("Your response will recommend another word to "
                                                                       "learn.")

    # append instructions to messages
    messages.append(learn_instruction)

    # get last messages
    try:
        with open(file_name) as user_file:
            data = json.load(user_file)

            # append las 5 items of data
            if data:
                if len(data) < 5:
                    for item in data:
                        messages.append(item)
                else:
                    for item in data[-5:]:
                        messages.append(item)
    except Exception as e:
        print(e)
        pass

    finally:
        return messages


# store messages
def store_messages(req_message, res_message):
    # define the file name
    file_name = "stored_data.json"

    # get recent messages getting off the system content
    messages = get_recent_messages()[1:]

    # add message to data
    user_message = {'role': 'user', 'content': req_message}
    assistant_message = {'role': 'assistant', 'content': res_message}

    messages.append(user_message)
    messages.append(assistant_message)

    # save messages in database file
    with open(file_name, 'w') as f:
        json.dump(messages, f)


# reset messages
def reset_messages():
    open("stored_data.json", "w")
