# Transformers & Prompt Engineering Reference Guide 


---

##  What is a Transformers Pipeline?

In Hugging Face's `transformers` library, a **Pipeline** is an abstraction layer that wraps all the complex steps required to make predictions using a machine learning model. It allows you to perform inference with just a few lines of code.

Rather than manually preparing text, tokenizing it, feeding it to the model, and decoding the output, the `pipeline()` object handles it all under the hood.

### The Pipeline Data Flow

```mermaid
graph TD
    InputText[Raw Input Text: 'I love learning!'] --> Tokenizer[1. Tokenizer: Converts text to numerical token IDs]
    Tokenizer --> Model[2. Model: Performs tensor calculations & predicts outputs]
    Model --> PostProcessor[3. Post-Processor: Converts raw predictions back to readable text/scores]
    PostProcessor --> FinalOutput[Final Output: Positive | 99.8%]

    style InputText fill:#f9f,stroke:#333,stroke-width:2px
    style FinalOutput fill:#bbf,stroke:#333,stroke-width:2px
```

1. **Tokenizer**: Translates raw text into input tokens (numerical IDs) that the neural network can process.
2. **Model**: Runs the neural network mathematical operations on the tokenized inputs.
3. **Post-Processor**: Translates raw model numbers (logits/probabilities) back into user-friendly Python dictionaries, scores, or text strings.

---

## 🛠️ Day 17: Transformers & Models

We explored three fundamental pipelines:

### 1. Text Generation (`gpt2`)
* **Purpose**: Generates coherent text continuing from a given starting prompt.
* **How it works**: Uses causal language modeling (predicting the next token) to generate text auto-regressively.
* **Code Example**:
  ```python
  generator = pipeline("text-generation", model="gpt2")
  output = generator("Artificial intelligence is", max_length=25)
  ```

### 2. Summarization (`distilbart`)
* **Purpose**: Condenses a long piece of text into a shorter, concise summary while maintaining the main context.
* **Model used**: `sshleifer/distilbart-cnn-12-6` (a fast, distilled version of BART trained on CNN news datasets).
* **Code Example**:
  ```python
  summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
  output = summarizer(long_text, max_length=15, min_length=5)
  ```

### 3. Classification / Sentiment Analysis (`distilbert`)
* **Purpose**: Assigns labels (like positive/negative sentiments) to text.
* **Model used**: `distilbert-base-uncased-finetuned-sst-2-english` (a lightweight BERT model fine-tuned on sentiment datasets).
* **Code Example**:
  ```python
  classifier = pipeline("sentiment-analysis", model="distilbert/distilbert-base-uncased-finetuned-sst-2-english")
  output = classifier("I absolutely love learning!")
  ```

---

## 💬 Day 18: Prompt Engineering

Prompt engineering is the practice of structuring text inputs (prompts) to guide Generative Models (LLMs) to perform specific tasks.

### 1. Zero-Shot Prompting
* **Definition**: Asking the model to perform a task directly without giving it any examples. We rely entirely on the model's pre-trained knowledge.
* **Example**:
  ```
  Classify the sentiment of this review as Positive or Negative:
  'The battery dies in 2 hours, totally useless!'
  ```

### 2. Few-Shot Prompting
* **Definition**: Providing the model with a few examples (demonstrations) of the input-output format before the actual query. This helps guide the model to output a specific format or follow a pattern.
* **Example**:
  ```
  Classify reviews like the examples below:
  Review: 'I love the high-quality screen.' -> Product: Screen | Sentiment: Positive
  Review: 'The buttons are hard to press.' -> Product: Buttons | Sentiment: Negative
  Review: 'The case scratches too easily.' -> 
  ```

### 3. System-level Persona Control
* **Definition**: Setting system-level instructions to instruct the model to adopt a specific persona, tone, or rule set (e.g., behaving as a Shakespearean actor, a pirate, or a concise code corrector).
* **API Structure**:
  ```python
  messages = [
      {"role": "system", "content": "You are a Shakespearean actor."},
      {"role": "user", "content": "What is Python?"}
  ]
  ```
