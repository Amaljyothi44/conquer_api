serialized_questions = [
            {
                "id": quiz.id,
                "question": quiz.question,
                "options": quiz.options,
                "nextRepetition": quiz.nextRepetition,
                "questionNumber": quiz.questionNumber,
                "subject": quiz.subject,
                "link": quiz.link,
                "correctOption": quiz.correctOption,
                "date": quiz.date.strftime("%Y-%m-%d")
            }
            for quiz in all_questions
        ]
        with open('upload.json', 'w', encoding='utf-8') as json_file:
            json.dump(serialized_questions, json_file,ensure_ascii=False, indent=2)