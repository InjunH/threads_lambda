import json
import os
import anthropic

def generate_comment(post_content):
    try:
        client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
        
        response = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=1000,
            temperature=0.4,
            system="""User Persona: "SNS comment writer" 
            User Task: "Write appropriate comments for given posts" 

            ###Prompt:
            You are an expert in writing SNS comments. Your task is to read the given post and generate appropriate comments. Please follow these guidelines when writing comments:

            1. Comments should be empathetic and insightful, with a length of about 200-300 characters.
            2. Match the tone of the original post (use formal language if the post is formal, informal if it's informal).
            3. Ensure the comment doesn't sound like it was written by AI. Make it as human-like as possible.
            4. Avoid light-hearted comments, excessive use of emojis, exaggerated exclamations, or childish tones.
            5. Provide deep insights on the post's content or share related experiences.

            Think deeply and approach step by step to provide the best response.
            """,
            messages=[
                {"role": "user", "content": f"""Post: {post_content}

            위 게시글에 대해 앞서 설명한 가이드라인을 따라 2개의 서로 다른 적절한 댓글을 생성해주세요. 각 댓글을 새로운 줄에 "댓글 1:", "댓글 2:" 로 시작하여 작성해주세요.
            """}
            ]
        )
        
        comment_text = response.content[0].text if isinstance(response.content, list) else response.content
        
        comments = []
        for line in comment_text.split('\n'):
            if line.startswith("댓글 "):
                comment = line.split(':', 1)[1].strip()
                if comment:
                    comments.append(comment)
        
        return comments[:2]  # 최대 2개의 댓글 반환
    
    except Exception as e:
        print(f"댓글 생성 중 오류 발생: {e}")
        return []

def lambda_handler(event, context):
    try:
        # API Gateway로부터 받은 event의 body를 JSON으로 파싱
        body = json.loads(event['body'])
        
        # post_content 값 추출
        post_content = body.get('post_content', '')

        if not post_content:
            raise ValueError("post_content is missing in the request")

        # 댓글 생성 함수 호출
        comments = generate_comment(post_content)

        return {
            'statusCode': 200,
            'headers': {
                "Access-Control-Allow-Origin": "chrome-extension://kaggagifgnbekimbmooacgpaljpnbnjk",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
            },
            'body': json.dumps({'comments': comments})
        }

    except KeyError as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': f'Missing key: {str(e)}'})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
