import streamlit as st

from mistralai import UserMessage
import streamlit as st
import os

import prompts


def story_generation(client):

    # Keep track of wether the story ahs already been written.
    if "written" not in st.session_state:
        st.session_state.written = False

    # Add header container
    st.title("Your Personal JournalAIst")
    st.write(
        """
        ### Please select the story type you would like me to write for you.
    """
    )
    """"
    # Create columns for horizontal layout
    col1, col2, col3 = st.columns(3)

    # Create radio buttons for each configuration option in separate columns
    with col1:
        st.session_state.CONFIG["style"] = st.radio(
            "Select the writing style:",
            ["Bill Bryson", "Hemingway", "J.K. Rowling", "Neil Gaiman"],
            index=["Bill Bryson", "Hemingway", "J.K. Rowling", "Neil Gaiman"].index(
                st.session_state.CONFIG["style"]
            ),
        )

    with col2:
        st.session_state.CONFIG["viewpoint"] = st.radio(
            "Select the viewpoint:",
            ["first-person", "second-person", "third-person"],
            index=["first-person", "second-person", "third-person"].index(
                st.session_state.CONFIG["viewpoint"]
            ),
        )

    #with col3:
    """
    st.session_state.CONFIG["story_type"] = st.radio(
        "Select the story type:",
        ["journal entry", "blog post", "short story", "article"],
        index=["journal entry", "blog post", "short story", "article"].index(
            st.session_state.CONFIG["story_type"]
        ),
    )

    
    start_writing_button = st.empty()
    start_writing = start_writing_button.button("Start writing!")

    if start_writing:
        st.session_state.written = True
        start_writing_button.empty()
        # Export conversation history
        with open(
            f"stories/{st.session_state.session_id}/conversation_history.txt", "w"
        ) as f:
            print("Exporting conversation history...")
            for message in st.session_state.messages:
                f.write(f"{message.role}: {message.content}\n")

        # Clear conversation history
        conversation_log = st.session_state.messages
        st.session_state.messages = []

        # Read the conversation log from the text file
        with open(
            f"stories/{st.session_state.session_id}/conversation_history.txt",
            "r",
        ) as f:
            conversation_text = f.read()

        # Use the Mistral API to generate a story based on the conversation log

        # story_prompt = f"Write a short, evocative story based on the following conversation log. Use markdown formatting where appropriate:\n\n{conversation_text}\n\nStory:"
        story_prompt_paths = {
            "article": "alt_prompts/story_teller/article.md",
            "blog post": "alt_prompts/story_teller/blog_post.md",
            "short story": "alt_prompts/story_teller/short_story.md",
            "journal entry": "alt_prompts/story_teller/journal_entry.md",
        }

        story_prompt = prompts.render_template_from_file(
            story_prompt_paths[st.session_state.CONFIG["story_type"]],
            # style=st.session_state.CONFIG['style'],
            # viewpoint=st.session_state.CONFIG['viewpoint'],
            # story_type=st.session_state.CONFIG['story_type'],
            background_info_interview=conversation_text,
            # TODO add pictures
            picture_information=st.session_state.picture_information,
            n_pictures=st.session_state.n_pictures,
        )

        # print(story_prompt)
        story_response = client.chat.complete(
            model=st.session_state["mistral_model"],
            messages=[UserMessage(role="user", content=story_prompt)],
        )
        story = story_response.choices[0].message.content

        # Save the story to a markdown file
        print(f"Saving story to stories/{st.session_state.session_id}/story.md")
        with open(f"stories/{st.session_state.session_id}/story.md", "w") as f:
            f.write(story)

        st.session_state.page = "final"
        st.rerun()
