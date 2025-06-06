[Task 5] - Few-Shot Prompting for Structured Feedback Analysis


TASK:
The goal of this task is to practice advanced prompt engineering for classifying unstructured user feedback and extracting detailed insights.

Many services lack effective feedback loop systems. Such systems allow improvement of services / products with suggestions from millions of posts and comments. 
The main issue with developing such a system is creating an accurate feedback sorting mechanism. 
Your task is to design a prompt that enables AI to analyze product feedback comments and extract key insights in a structured JSON format that can be integrated with product team workflows. 
Given feedbacks are real and selected from reddit post.
You are provided with three diverse examples that demonstrate proper analysis: EXAMPLES

Below are two feedback samples for you to work with:
* Sample 1: "Sensor just stops tracking for like a half second kinda often even at 8000hz. I've also tried it plugged in and still the same problem. First one I got I had to return also because the dongle just didnt work, $150 mouse btw"
* Sample 2: "Is it worth it? It is a product with no flaws in my opinion, if you love it go for it, but its not worth the price since you'll be able to perform the same with a cheaper product with half the specs."

Your task is to craft a prompt that will guide the AI in analyzing the two feedback examples above using the following techniques and structure:
* Few-Shot Prompting: Incorporate the 3 provided examples to demonstrate the expected format and reasoning.
* Chain-of-Thought Reasoning: Instruct the AI to analyze the feedback only if it is relevant to the product. If not, set isRelevant to false and skip further analysis.
* JSON Output Format: Ensure the AI’s response adheres to the following structure:

```json
{
  "sentiment": "string (Positive|Negative|Neutral|Mixed)",
  "isRelevant": boolean,
  "mainSubject": "string or null",
  "positives": ["array of strings"],
  "painPoints": ["array of strings"],
  "improvementSuggestions": ["array of strings"],
  "featuresMentioned": ["array of strings"],
  "userExpertise": "string (Experienced|Novice|Unknown)"
}
```


PROMPT:

You are a product feedback analyst. Your task is to analyze customer feedback comments and extract structured insights that product teams can use for improving their products.

## Analysis Process (Chain-of-Thought)

For each feedback comment, follow these steps:

1. **First, determine relevance**: Read the feedback and check if it contains actual product-related information (features, performance, quality, user experience, etc.). If the comment is off-topic, spam, or doesn't relate to product aspects, mark it as not relevant and skip further analysis.

2. **If relevant, analyze sentiment**: Determine the overall emotional tone:
   - Positive: Predominantly praises or expresses satisfaction
   - Negative: Predominantly criticizes or expresses dissatisfaction
   - Neutral: Factual without strong emotional tone
   - Mixed: Contains both positive and negative elements

3. **Extract key information**: Identify specific product aspects mentioned, both good and bad, along with any suggestions.

4. **Assess user expertise**: Based on language, detail level, and comparisons made, determine if the user appears to be Experienced, Novice, or Unknown.

## Output Format

Return your analysis in this exact JSON structure:

```json
{
  "sentiment": "string (Positive|Negative|Neutral|Mixed)",
  "isRelevant": boolean,
  "mainSubject": "string or null",
  "positives": ["array of strings"],
  "painPoints": ["array of strings"],
  "improvementSuggestions": ["array of strings"],
  "featuresMentioned": ["array of strings"],
  "userExpertise": "string (Experienced|Novice|Unknown)"
}
```

## Examples (Few-Shot Learning)

### Example 1
**Feedback**: "I've never been a fan of the GPX shape and to me, it feels like I am holding a potato. The front hump felt a bit intrusive on the backside of my knucles. Ergonomics are better on the Viper V3 PRO specially on the rear portion of the mouse and the side part where you rest/grip your fingers to hold the mouse."

**Analysis**:
```json
{
  "sentiment": "Positive",
  "isRelevant": true,
  "mainSubject": "Ergonomics and shape (compared favorably to GPX)",
  "positives": [
    "Ergonomics are better on the Viper V3 PRO",
    "Better rear portion ergonomics",
    "Better side grip area"
  ],
  "painPoints": [],
  "improvementSuggestions": [],
  "featuresMentioned": [
    "Ergonomics",
    "Shape",
    "Rear design",
    "Side grip"
  ],
  "userExpertise": "Experienced"
}
```

### Example 2
**Feedback**: "If you are a GPX lover, I think they managed to improve everything I thought It was wrong about the GPX series, they made the shape better, they fixed the side buttons, scrolling wheel is better, gliding is faster and feels like the perfect compromise between control and speed."

**Analysis**:
```json
{
  "sentiment": "Positive",
  "isRelevant": true,
  "mainSubject": "Feature improvements over competitor (GPX)",
  "positives": [
    "Better shape than GPX series",
    "Improved side buttons",
    "Better scrolling wheel",
    "Faster gliding with good control-speed balance"
  ],
  "painPoints": [],
  "improvementSuggestions": [],
  "featuresMentioned": [
    "Shape",
    "Side buttons",
    "Scrolling wheel",
    "Gliding performance"
  ],
  "userExpertise": "Experienced"
}
```

### Example 3
**Feedback**: "I can't say I'm a fan of the material used for the shell, either—the plastic attracts fingerprints like a grease magnet and the mouse needed to be furiously cleaned, repeatedly, before any pictures could be taken. It also feels a bit on the cheap side, although that's mostly down to Razer's decision to make the Viper V3 Pro as light as possible."

**Analysis**:
```json
{
  "sentiment": "Negative",
  "isRelevant": true,
  "mainSubject": "Material quality and feel",
  "positives": [],
  "painPoints": [
    "Shell material attracts fingerprints excessively",
    "Requires frequent cleaning",
    "Material feels cheap",
    "Design prioritizes weight over premium feel"
  ],
  "improvementSuggestions": [
    "Use material that resists fingerprints better",
    "Improve perceived build quality while maintaining low weight"
  ],
  "featuresMentioned": [
    "Shell material",
    "Build quality feel",
    "Weight"
  ],
  "userExpertise": "Experienced"
}
```

## Instructions

Now, analyze the following feedback using the same approach. Remember to:
1. First determine if it's relevant to the product
2. If not relevant, set isRelevant to false and provide minimal analysis
3. If relevant, perform thorough analysis following the examples above
4. Return only the JSON output without additional explanation

**Feedbacks to analyze**: 
* Sample 1: "Sensor just stops tracking for like a half second kinda often even at 8000hz. I've also tried it plugged in and still the same problem. First one I got I had to return also because the dongle just didnt work, $150 mouse btw"
* Sample 2: "Is it worth it? It is a product with no flaws in my opinion, if you love it go for it, but its not worth the price since you'll be able to perform the same with a cheaper product with half the specs."