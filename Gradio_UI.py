import gradio as gr

from smolagents import stream_to_gradio


class GradioUI:

    def __init__(self, agent):

        self.agent = agent


    # ============================================================
    # RESPOND
    # ============================================================

    def respond(
        self,
        message,
        history
    ):

        if not message or not message.strip():

            yield history or [], ""

            return

        # Make sure history is always a list.
        if history is None:
            history = []

        messages = list(history)

        # Add the user's message immediately.
        messages.append(
            {
                "role": "user",
                "content": message.strip()
            }
        )

        # First yield:
        # 1. Show the user's message.
        # 2. CLEAR THE INPUT BOX.
        #
        # This fixes the textbox remaining filled.
        yield messages, ""

        try:

            for msg in stream_to_gradio(
                self.agent,
                task=message.strip(),
                reset_agent_memory=False
            ):

                # ------------------------------------------------
                # ChatMessage -> dictionary
                # ------------------------------------------------

                if (
                    hasattr(msg, "role")
                    and hasattr(msg, "content")
                ):

                    role = msg.role

                    if hasattr(
                        role,
                        "value"
                    ):

                        role = role.value

                    messages.append(
                        {
                            "role": str(role),
                            "content": msg.content
                        }
                    )

                elif isinstance(
                    msg,
                    dict
                ):

                    # Make sure the dictionary has
                    # a valid role/content structure.
                    if (
                        "role" in msg
                        and "content" in msg
                    ):

                        messages.append(
                            {
                                "role": msg["role"],
                                "content": msg["content"]
                            }
                        )

                    else:

                        messages.append(
                            {
                                "role": "assistant",
                                "content": str(msg)
                            }
                        )

                else:

                    messages.append(
                        {
                            "role": "assistant",
                            "content": str(msg)
                        }
                    )

                # Keep textbox empty throughout generation.
                yield messages, ""

        except Exception as e:

            messages.append(
                {
                    "role": "assistant",
                    "content": (
                        "### Agent Error\n\n"
                        f"`{type(e).__name__}`\n\n"
                        f"{str(e)}"
                    )
                }
            )

            yield messages, ""


    # ============================================================
    # LAUNCH
    # ============================================================

    def launch(
        self,
        share=True,
        **kwargs
    ):

        # ========================================================
        # CSS
        # ========================================================

        css = """

        /* ======================================================
           GLOBAL
           ====================================================== */

        * {
            font-family:
                "Segoe UI",
                Arial,
                sans-serif !important;

            box-sizing:
                border-box !important;
        }


        html,
        body {

            width: 100% !important;
            min-width: 100% !important;

            margin: 0 !important;
            padding: 0 !important;

            background:
                #08111f !important;
        }


        .gradio-container {

            width: 100vw !important;
            max-width: none !important;
            min-width: 100vw !important;

            margin: 0 !important;
            padding: 0 !important;

            background:
                #08111f !important;
        }


        .gradio-container > div {

            width: 100% !important;
            max-width: none !important;

            margin: 0 !important;
        }


        .gradio-row {

            width: 100% !important;
            max-width: none !important;

            margin: 0 !important;
        }


        .gradio-column {

            max-width: none !important;
        }


        .gradio-container *,
        .gradio-container::before,
        .gradio-container::after {

            background-image:
                none !important;
        }


        /* ======================================================
           HEADER
           ====================================================== */

        .repopilot-header {

            width: 100% !important;

            padding:
                28px
                40px
                22px
                40px;

            border-bottom:
                1px solid #1d3048;

            background:
                #0b1b33;
        }


        .brand-title {

            font-size: 28px;

            font-weight: 600;

            color:
                #f1f5f9;

            letter-spacing:
                -0.7px;
        }


        .brand-subtitle {

            color:
                #91a4ba;

            font-size:
                14px;

            margin-top:
                3px;
        }


        .status {

            display:
                inline-flex;

            align-items:
                center;

            gap:
                7px;

            margin-top:
                16px;

            padding:
                6px 11px;

            border-radius:
                999px;

            background:
                #10233d;

            border:
                1px solid #1e3a5f;

            color:
                #9fb2c8;

            font-size:
                12px;
        }


        .status-dot {

            width:
                7px;

            height:
                7px;

            border-radius:
                50%;

            background:
                #35c46a;
        }


        /* ======================================================
           WHAT REP0PILOT CAN DO
           ====================================================== */

        .capabilities {

            width:
                100% !important;

            padding:
                18px 40px;

            background:
                #0a1729;

            border-bottom:
                1px solid #1d3048;

            color:
                #8fa3b9;

            font-size:
                13px;

            line-height:
                1.65;
        }


        .capabilities strong {

            color:
                #dce7f3;

            font-weight:
                600;
        }


        /* ======================================================
           MAIN
           ====================================================== */

        .main-layout {

            width:
                100% !important;

            margin:
                0 !important;

            padding:
                0 !important;
        }


        /* ======================================================
           SIDEBAR
           ====================================================== */

        .sidebar {

            background:
                #0a1729;

            border-right:
                1px solid #1d3048;

            min-height:
                calc(100vh - 210px);

            padding:
                28px 25px;

            margin:
                0 !important;
        }


        .sidebar-title {

            color:
                #e5edf7;

            font-size:
                15px;

            font-weight:
                600;

            margin-bottom:
                8px;
        }


        .feature {

            padding:
                12px 0;

            border-bottom:
                1px solid #17283e;

            color:
                #b5c3d3;

            font-size:
                13px;
        }


        .model-box {

            margin-top:
                20px;

            padding:
                13px;

            border-radius:
                9px;

            background:
                #0d1d32;

            border:
                1px solid #1b3049;
        }


        .model-label {

            color:
                #687d95;

            font-size:
                11px;

            font-weight:
                600;

            text-transform:
                uppercase;

            letter-spacing:
                .6px;
        }


        .model-name {

            color:
                #cbd8e6;

            font-size:
                12px;

            margin-top:
                5px;

            word-break:
                break-word;
        }


        /* ======================================================
           CHAT
           ====================================================== */

        .chat-column {

            background:
                #08111f;

            min-height:
                calc(100vh - 210px);

            padding:
                0 !important;

            margin:
                0 !important;
        }


        #chatbot {

            width:
                100% !important;

            border:
                none !important;

            background:
                #08111f !important;

            border-radius:
                0 !important;

            /*
               Space at the bottom so the fixed input bar
               does not cover the final messages.
            */
            padding-bottom:
                130px !important;
        }


        #chatbot .message {

            font-size:
                14px !important;

            line-height:
                1.6 !important;
        }


        /* ======================================================
           QUICK ACTIONS
           ====================================================== */

        .quick-actions {

            padding:
                12px 25px;

            border-top:
                1px solid #14243a;

            background:
                #08111f;
        }


        .quick-title {

            color:
                #657b93;

            font-size:
                11px;

            margin-bottom:
                8px;
        }


        .quick-btn {

            border:
                1px solid #29415f !important;

            background:
                #0d1d32 !important;

            color:
                #aebed0 !important;

            font-size:
                12px !important;

            border-radius:
                8px !important;
        }


        .quick-btn:hover {

            border-color:
                #3b6090 !important;

            color:
                #e2eaf3 !important;
        }


        /* ======================================================
           FIXED INPUT
           ====================================================== */

        .input-area {

            position:
                fixed !important;

            bottom:
                0 !important;

            right:
                0 !important;

            width:
                calc(100% - 270px) !important;

            z-index:
                1000 !important;

            padding:
                12px 35px 18px 35px;

            border-top:
                1px solid #1d3048;

            background:
                #08111f !important;

            margin:
                0 !important;
        }


        #prompt-box {

            width:
                100% !important;

            border:
                1px solid #29415f !important;

            border-radius:
                12px !important;

            background:
                #0d1d32 !important;

            box-shadow:
                none !important;
        }


        #prompt-box textarea {

            background:
                #0d1d32 !important;

            color:
                #e5edf7 !important;

            border:
                none !important;

            border-radius:
                12px !important;

            font-size:
                14px !important;

            line-height:
                1.5 !important;

            padding:
                14px 16px !important;

            resize:
                none !important;
        }


        #prompt-box textarea::placeholder {

            color:
                #657b93 !important;

            opacity:
                1 !important;
        }


        #prompt-box:focus-within {

            border-color:
                #3b6090 !important;

            box-shadow:
                0 0 0 1px #3b6090 !important;
        }


        /* ======================================================
           SEND BUTTON
           ====================================================== */

        #send-button {

            display:
                none !important;
        }


        /* ======================================================
           FOOTER
           ====================================================== */

        .footer {

            width:
                100%;

            text-align:
                center;

            padding:
                14px;

            color:
                #53677d;

            font-size:
                11px;

            border-top:
                1px solid #14243a;

            background:
                #08111f;
        }


        /* ======================================================
           MOBILE
           ====================================================== */

        @media (max-width: 800px) {

            .repopilot-header {

                padding:
                    22px 20px 18px 20px;
            }


            .capabilities {

                padding:
                    15px 20px;
            }


            .sidebar {

                display:
                    none !important;
            }


            .input-area {

                width:
                    100% !important;

                padding:
                    12px 15px 18px 15px;
            }


            #chatbot {

                padding-bottom:
                    130px !important;
            }


            .brand-title {

                font-size:
                    24px;
            }


            .brand-subtitle {

                font-size:
                    12px;
            }
        }

        """


        # ========================================================
        # JAVASCRIPT
        # ========================================================

        js = """

        () => {

            /*
             * Gradio's multiline textbox normally treats Enter
             * as a newline.
             *
             * RepoPilot behavior:
             *
             * Enter       -> SEND
             * Shift+Enter -> NEW LINE
             */

            /*
             * Listen on document during capture, before
             * Gradio's textbox handler sees the key event.
             */
            document.addEventListener(
                "keydown",
                function(event) {

                    if (
                        event.key !== "Enter" ||
                        !event.target.closest("#prompt-box")
                    ) {
                        return;
                    }

                    /* Shift+Enter must remain a normal newline. */
                    if (event.shiftKey) {
                        event.stopImmediatePropagation();
                        return;
                    }

                    /* Enter sends without adding a newline. */
                    event.preventDefault();
                    event.stopImmediatePropagation();

                    const sendButton =
                        document.querySelector("#send-button");

                    if (sendButton) {
                        sendButton.click();
                    }
                },
                true
            );

        }

        """


        # ========================================================
        # GRADIO APP
        # ========================================================

        with gr.Blocks(
            title="RepoPilot",
            css=css,
            js=js,
            theme=gr.themes.Base(
                primary_hue="blue",
                neutral_hue="slate"
            )
        ) as demo:

            # ----------------------------------------------------
            # HEADER
            # ----------------------------------------------------

            gr.HTML(
                """
                <div class="repopilot-header">

                    <div class="brand-title">
                        RepoPilot
                    </div>

                    <div class="brand-subtitle">
                        AI-powered GitHub repository analyst,
                        by Mohamed Faheem
                    </div>

                    <div class="status">

                        <span class="status-dot"></span>

                        Agent ready

                    </div>

                </div>
                """
            )


            # ----------------------------------------------------
            # CAPABILITIES PARAGRAPH
            # ----------------------------------------------------

            gr.HTML(
                """
                <div class="capabilities">

                    <strong>What RepoPilot can do:</strong>
                    Give it a public GitHub repository and ask
                    questions about it. RepoPilot can inspect the
                    repository structure, count files and folders,
                    identify technologies, explain architecture,
                    inspect source code, analyse backend logic,
                    find contributors, search for files and explain
                    how different parts of a project work. It uses
                    Ollama to run the AI model locally on your PC.

                </div>
                """
            )


            # ----------------------------------------------------
            # MAIN LAYOUT
            # ----------------------------------------------------

            with gr.Row(
                equal_height=False,
                elem_classes="main-layout"
            ):


                # =================================================
                # SIDEBAR
                # =================================================

                with gr.Column(
                    scale=1,
                    min_width=270,
                    elem_classes="sidebar"
                ):

                    gr.HTML(
                        """
                        <div class="sidebar-title">
                            RepoPilot tools
                        </div>

                        <div class="feature">
                            Repository overview
                        </div>

                        <div class="feature">
                            File & folder analysis
                        </div>

                        <div class="feature">
                            Source-code inspection
                        </div>

                        <div class="feature">
                            Architecture analysis
                        </div>

                        <div class="feature">
                            Backend analysis
                        </div>

                        <div class="feature">
                            Contributor detection
                        </div>

                        <div class="feature">
                            Repository search
                        </div>

                        <div class="model-box">

                            <div class="model-label">
                                AI Model
                            </div>

                            <div class="model-name">
                                qwen2.5-coder:7b
                            </div>

                        </div>

                        <div class="model-box">

                            <div class="model-label">
                                Runtime
                            </div>

                            <div class="model-name">
                                Ollama · Local PC
                            </div>

                        </div>

                        <div class="model-box">

                            <div class="model-label">
                                Agent Framework
                            </div>

                            <div class="model-name">
                                Hugging Face smolagents
                            </div>

                        </div>
                        """
                    )


                # =================================================
                # CHAT
                # =================================================

                with gr.Column(
                    scale=4,
                    elem_classes="chat-column"
                ):

                    chatbot = gr.Chatbot(
                        label="RepoPilot",
                        height=650,
                        show_label=False,
                        elem_id="chatbot"
                    )


                    # ------------------------------------------------
                    # QUICK ACTIONS
                    # ------------------------------------------------

                    with gr.Column(
                        elem_classes="quick-actions"
                    ):

                        gr.HTML(
                            """
                            <div class="quick-title">
                                Quick questions
                            </div>
                            """
                        )

                        with gr.Row():

                            overview_btn = gr.Button(
                                "Explain repository",
                                elem_classes="quick-btn"
                            )

                            files_btn = gr.Button(
                                "Count files",
                                elem_classes="quick-btn"
                            )

                            contributors_btn = gr.Button(
                                "Contributors",
                                elem_classes="quick-btn"
                            )

                            architecture_btn = gr.Button(
                                "Architecture",
                                elem_classes="quick-btn"
                            )


                    # ------------------------------------------------
                    # FIXED INPUT
                    # ------------------------------------------------

                    with gr.Row(
                        elem_classes="input-area"
                    ):

                        prompt = gr.Textbox(

                            placeholder=(
                                "Paste a GitHub repository URL "
                                "and ask RepoPilot what you "
                                "want to know..."
                            ),

                            show_label=False,

                            lines=2,

                            max_lines=8,

                            elem_id="prompt-box",

                            autofocus=True
                        )


                    # ------------------------------------------------
                    # HIDDEN SEND BUTTON
                    # ------------------------------------------------

                    send_button = gr.Button(
                        "Send",
                        elem_id="send-button"
                    )


                    # ------------------------------------------------
                    # FOOTER
                    # ------------------------------------------------

                    gr.HTML(
                        """
                        <div class="footer">

                            RepoPilot · Built with Python,
                            Gradio, Ollama and
                            Hugging Face smolagents

                        </div>
                        """
                    )


            # ========================================================
            # SEND EVENT
            # ========================================================

            # IMPORTANT:
            #
            # We now output TWO things:
            #
            # 1. chatbot
            # 2. prompt
            #
            # The second output is ""
            # which clears the textbox.

            send_event = prompt.submit(
                self.respond,

                inputs=[
                    prompt,
                    chatbot
                ],

                outputs=[
                    chatbot,
                    prompt
                ]
            )


            # --------------------------------------------------------
            # Hidden button uses the EXACT SAME submit event.
            # --------------------------------------------------------

            send_button.click(
                self.respond,

                inputs=[
                    prompt,
                    chatbot
                ],

                outputs=[
                    chatbot,
                    prompt
                ]
            )


            # ========================================================
            # QUICK ACTION BUTTONS
            # ========================================================

            def set_prompt(text):
                return text


            overview_btn.click(
                lambda: (
                    "Paste the GitHub repository URL here, "
                    "then explain this repository in short."
                ),
                outputs=prompt
            )


            files_btn.click(
                lambda: (
                    "Paste the GitHub repository URL here, "
                    "then tell me the total number of files "
                    "and folders."
                ),
                outputs=prompt
            )


            contributors_btn.click(
                lambda: (
                    "Paste the GitHub repository URL here, "
                    "then tell me who the contributors are."
                ),
                outputs=prompt
            )


            architecture_btn.click(
                lambda: (
                    "Paste the GitHub repository URL here, "
                    "then explain the architecture and how "
                    "the main components work together."
                ),
                outputs=prompt
            )


        # ========================================================
        # LAUNCH
        # ========================================================

        demo.launch(

            share=share,

            **kwargs
        )
