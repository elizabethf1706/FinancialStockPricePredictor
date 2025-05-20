from groq import Groq

def advise_earnings_from_query(GROQ_API_KEY, stock_keyword, query_results, user_question):
    client = Groq(api_key=GROQ_API_KEY)
    documents = query_results["documents"][0]
    speaker_title = query_results["metadatas"][0]

    content = ""
    
    for passage in range(len(documents)):
        entry = f"{speaker_title[passage]['speaker']} ({speaker_title[passage]['title']}): \n {documents[passage]} \n\n"
        content += entry
    
    response = client.chat.completions.create(
        model = "llama3-70b-8192",
        messages=[{
            "role": "user",
            "content": f"""Using only the following excerpts from {stock_keyword}'s most recent earnings call transcript, 
                        provide a direct and well-supported answer to the user’s question: '{user_question}'. Base your response 
                        strictly on the information in the excerpts. Here are the excerpts: {content}. Whenever you refer
                        to the provided texts, instead say the most recent earnings calls. When you can, use numbered points."""
        }],
        temperature = 0
    )
    
    return response.choices[0].message.content