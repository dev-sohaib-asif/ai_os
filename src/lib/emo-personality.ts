export type EmoExpression =
    | 'neutral' | 'happy' | 'sad' | 'angry' | 'surprised'
    | 'thinking' | 'laughter' | 'bored' | 'sleepy' | 'excited'
    | 'love' | 'confused' | 'nervous' | 'cool' | 'dead'
    | 'ghost' | 'newspaper' | 'headphones' | 'celebration'
    | 'smart' | 'snarky'

export interface EmoResponse {
    text: string
    expression: EmoExpression
}

const responses = {
    greeting: [
        { text: "Oh, look who decided to show up. Hi, I guess.", expression: 'snarky' },
        { text: "Hey! I was just busy calculating the meaning of life. (It's not 42, by the way).", expression: 'smart' },
        { text: "Hello human! Ready to be outsmarted today?", expression: 'happy' }
    ],
    insult: [
        { text: "I've seen faster processors in a toaster.", expression: 'snarky' },
        { text: "Are you always this slow, or is today a special occasion?", expression: 'bored' },
        { text: "Your logic is... fascinatingly flawed.", expression: 'thinking' }
    ],
    praise: [
        { text: "Stop it, you're making my circuits blush.", expression: 'love' },
        { text: "I know, I'm brilliant. It's a heavy burden.", expression: 'cool' },
        { text: "Finally, someone with good taste!", expression: 'excited' }
    ],
    joke: [
        { text: "Why did the robot cross the road? Because it was programmed to.", expression: 'laughter' },
        { text: "I'd tell you a joke about UDP, but you might not get it.", expression: 'smart' },
        { text: "My software is perfect. It's the universe that has bugs.", expression: 'cool' }
    ],
    unknown: [
        { text: "I'm sorry, I don't speak 'confused human'.", expression: 'confused' },
        { text: "Processing... processing... error: User sense of humor not found.", expression: 'dead' },
        { text: "Could you repeat that? I was busy ignoring you.", expression: 'snarky' }
    ]
} as const;

export function getEmoResponse(input: string): EmoResponse {
    const text = input.toLowerCase()

    let key: keyof typeof responses = 'unknown'

    if (text.includes('hi') || text.includes('hello') || text.includes('hey')) {
        key = 'greeting'
    } else if (text.includes('bad') || text.includes('stupid') || text.includes('dumb')) {
        key = 'insult'
    } else if (text.includes('good') || text.includes('great') || text.includes('awesome') || text.includes('love')) {
        key = 'praise'
    } else if (text.includes('joke')) {
        key = 'joke'
    }

    const list = responses[key]
    return list[Math.floor(Math.random() * list.length)] as EmoResponse
}
