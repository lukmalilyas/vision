
#SAMPLE CODE TO FINE TUNE DEEPSPEECH MODEL
import deepspeech

def fine_tune_model(train_csv, dev_csv, checkpoint_dir, epochs):
    # Load the pre-trained model
    model = deepspeech.Model('C:/Users/Acer/PycharmProjects/DeepSpeech/deepspeech-0.9.3-models.pbmm')

    # Fine-tune the model
    model.finetune(
        train_csv,
        dev_csv,
        epochs,
        checkpoint_dir
    )

    # Save the fine-tuned model
    model.save_checkpoint(checkpoint_dir)

if __name__ == "__main__":
    train_csv = 'C:/Users/Acer/Downloads/Recipes/csv/train.csv'
    dev_csv = 'C:/Users/Acer/Downloads/Recipes/csv/dev.csv'
    checkpoint_dir = 'C:/Users/Acer/PycharmProjects/DeepSpeech/deepspeech-0.9.2-checkpoint.tar.gz'
    epochs = 50

    fine_tune_model(train_csv, dev_csv, checkpoint_dir, epochs)

def evaluate_model(test_csv, checkpoint_dir):
    # Load the fine-tuned model
    model = deepspeech.Model('C:/Users/Acer/PycharmProjects/DeepSpeech/deepspeech-0.9.3-models.pbmm')

    # Evaluate the model
    results = model.evaluate(test_csv)

    print(f'WER: {results["wer"]}, CER: {results["cer"]}')

if __name__ == "__main__":
    test_csv = 'C:/Users/Acer/Downloads/Recipes/csv/test.csv'

    evaluate_model(test_csv, checkpoint_dir)
