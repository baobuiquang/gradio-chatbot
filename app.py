import gradio as gr
import time
import _response

global_suggestions = [""]

def chatbot_response(message, history):
    response, suggestions = _response.generate_response(message)
    # Suggestions
    global_suggestions.append(suggestions)
    # Return
    for i in range(len(response)):
        time.sleep(0.02)
        yield response[: i+1]

def change_suggestions():
    time.sleep(1)
    suggs = global_suggestions[-1]
    return gr.Dataset(samples=suggs)

e_chatbot = gr.Chatbot(
    elem_id = "gr_e_chatbot",
    layout = 'bubble',
    bubble_full_width = False,
    likeable = True,
    show_copy_button = True,
    show_copy_all_button = True,
    avatar_images = (
        'assets/user.png',
        'assets/bot.png',
    ),
    value = [
        [
            None, 
            "Chào bạn. Mình là chatbot trợ giúp tìm kiếm thông tin.",
        ],
        [
            None, 
            "Bạn hãy đặt câu hỏi ở khung phía dưới nhé!",
        ],
    ],
)
e_textbox = gr.Textbox(
    placeholder = "Nhập câu hỏi...",
    scale = 9,
)
e_button  = gr.Button(
    value = "Gửi",
    scale = 1,
)

with gr.Blocks(
    theme = gr.themes.Base(
        primary_hue = "stone",
    ),
    css = '\
        footer { display: none !important; visibility: hidden; opacity: 0.0; } \
        [data-testid="block-label"] { display: none; visibility: hidden; opacity: 0.0; } \
        #gr_e_chatbot { flex-grow: 1; height: 0px !important; } \
        .gradio-container .main .wrap .contain .gap { flex-grow: 1; } \
        .avatar-image { padding: 3px; } \
    ',
) as demo:
    e1 = gr.ChatInterface(
        fn=chatbot_response,
        chatbot = e_chatbot,
        textbox = e_textbox,
        submit_btn = e_button,
        stop_btn = "Dừng",
        retry_btn = "🔄️ Thử lại",
        undo_btn = "↩️ Hoàn tác",
        clear_btn = "🗑️ Xoá toàn bộ",
        autofocus = True,
    )
    e2 = gr.Examples(
        examples = [["Câu hỏi mẫu 1"], ["Câu hỏi mẫu 2"]], 
        inputs = e_textbox,
        label = "Câu hỏi gợi ý",
    )
    e_textbox.submit(change_suggestions, None, e2.dataset)
    e_button.click(change_suggestions, None, e2.dataset)

demo.launch(debug = False, share = False)