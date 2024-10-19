from flask import Flask, jsonify, render_template, request
import re
import random

app = Flask(__name__)
# Define response patterns and their corresponding responses
patterns_responses = {
    r".*I am feeling (.*)": [
        "Please tell me more about why you are feeling {}.",
        "What made you feel {}?",
        "How long have you been feeling {}?",
        "What do you think causes you to feel {}?",
        "Have you shared with anyone about feeling {}?",
        "Has feeling {} affected your routine?",
        "Do you want to feel differently than {}?",
        "What do you normally do when you feel {}?",
        "Have you noticed any patterns with feeling {}?",
        "What triggers this feeling of {}?",
    ],
    r".*I am (.*)": [
        "Why do you say you are {}?",
        "Do you feel being {} is affecting your day-to-day life?",
        "What does being {} mean to you?",
        "What makes you identify as {}?",
        "How does being {} impact your interactions with others?",
        "Have you always seen yourself as {}?",
        "Is there something you'd like to change about being {}?",
        "How has being {} shaped your experiences?",
        "Does being {} give you any sense of comfort or distress?",
    ],
    r".*I feel (.*)": [
        "What’s making you feel {}?",
        "Does feeling {} impact other parts of your life?",
        "Why do you think you feel {}?",
        "Is feeling {} a frequent occurrence for you?",
        "How do you handle feeling {}?",
        "What helps you manage feeling {}?",
        "Can you pinpoint when you started feeling {}?",
        "Is feeling {} connected to any particular event or person?",
        "Have you ever tried to avoid feeling {}?",
        "How would you like to handle feeling {} in the future?",
    ],
    r".*I have been (.*)": [
        "Can you explain why you've been {}?",
        "How does it make you feel to be {}?",
        "Have you been feeling {} for a long time?",
        "What has contributed to you being {}?",
        "Do you think being {} is something you can control?",
        "What do others say about you being {}?",
        "Has being {} impacted your mental state?",
        "Have you noticed any changes since being {}?",
        "Is being {} affecting your goals?",
        "How do you think being {} will shape your future?",
    ],
    r".*I think (.*)": [
        "What makes you think {}?",
        "Why do you believe {}?",
        "Do you often think {}?",
        "Has this thought about {} been constant?",
        "Is thinking {} helpful for you?",
        "Do you feel conflicted about thinking {}?",
        "What brought you to think {}?",
        "Would you like to change your thoughts about {}?",
        "Is thinking {} empowering or discouraging for you?",
        "How do you process thinking {}?",
    ],
    r".*I cannot (.*)": [
        "What do you think is stopping you from {}?",
        "Why do you believe you cannot {}?",
        "Have you tried to {} before?",
        "Is there a specific reason you think you can't {}?",
        "Have you asked for help to {}?",
        "What would make you feel capable of {}?",
        "How important is it for you to {}?",
        "Do you feel pressured by not being able to {}?",
        "Is it possible that you can {} with the right support?",
        "What would change if you were able to {}?",
    ],
    r".*I worry about (.*)": [
        "Why are you worried about {}?",
        "How often do you worry about {}?",
        "Do you think your worry about {} is justified?",
        "What can be done to address your worry about {}?",
        "Is worrying about {} affecting your daily life?",
        "Has worrying about {} become a habit?",
        "Is there someone you can talk to about {}?",
        "What happens when you try not to worry about {}?",
        "Do you think worrying about {} will help?",
        "What steps can you take to reduce your worry about {}?",
    ],
    r".*I struggle with (.*)": [
        "Tell me more about your struggles with {}.",
        "What makes {} challenging for you?",
        "How do you usually cope with {}?",
        "How long have you struggled with {}?",
        "Is struggling with {} impacting your mood?",
        "What has helped you in the past with {}?",
        "Do you feel like you're making progress with {}?",
        "How does struggling with {} affect your goals?",
        "Have you tried a different approach to {}?",
        "What would ease your struggle with {}?",
    ],
    r".*I am afraid of (.*)": [
        "What makes you afraid of {}?",
        "How does this fear of {} affect you?",
        "Have you always been afraid of {}?",
        "What can help reduce your fear of {}?",
        "Is your fear of {} affecting other areas of your life?",
        "Do you think facing {} would reduce your fear?",
        "Have you talked to someone about being afraid of {}?",
        "How would your life improve without fear of {}?",
        "What’s the worst thing that could happen with {}?",
        "Has your fear of {} changed over time?",
    ],
    r".*I wish (.*)": [
        "Why do you wish {}?",
        "Do you believe achieving {} will make you happier?",
        "What’s stopping you from {}?",
        "How would your life change if you got {}?",
        "What does {} represent for you?",
        "Do you think {} is achievable for you?",
        "How would you feel if {} happened?",
        "Have you made steps towards achieving {}?",
        "What would life look like if {} didn’t happen?",
        "Can you control whether {} happens or not?",
    ],
    r".*I need (.*)": [
        "What makes you feel like you need {}?",
        "How would {} help your current situation?",
        "Do you think it’s possible to get {}?",
        "What would change if you had {}?",
        "Is needing {} causing you stress?",
        "How does needing {} impact your decision-making?",
        "Have you talked to anyone about needing {}?",
        "What can you do to get closer to having {}?",
        "Is there an alternative to needing {}?",
        "How would your life improve if you didn’t need {}?",
    ],
    r".*I don't like (.*)": [
        "Why don’t you like {}?",
        "How do you feel when you encounter {}?",
        "Have you always disliked {}?",
        "What specifically about {} bothers you?",
        "Do you think not liking {} is affecting you?",
        "Have you tried changing your perspective on {}?",
        "Is it common for others to dislike {} as well?",
        "What would make {} more tolerable for you?",
        "Has your dislike for {} intensified?",
        "Do you avoid {} because of how you feel?",
    ],
    r".*I can't (.*)": [
        "Why do you think you can’t {}?",
        "What’s preventing you from {}?",
        "Have you tried to {} before?",
        "What would change if you could {}?",
        "Is it a fear that you can’t {}?",
        "Has someone told you that you can’t {}?",
        "What support do you need to {}?",
        "Do you want to be able to {}?",
        "What happens when you try to {}?",
        "Is there a specific obstacle in the way of {}?",
    ],
    r".*I hate (.*)": [
        "What makes you hate {}?",
        "Has this hatred towards {} been present for long?",
        "Why do you think you hate {}?",
        "Is hating {} affecting your peace of mind?",
        "Does hatred for {} impact your relationships?",
        "Can you identify why you feel hatred towards {}?",
        "Do you think you can overcome your hatred for {}?",
        "How does hating {} make you feel in the long run?",
        "Does hatred for {} control your actions?",
        "Has anything positive ever come from hating {}?",
    ],
    r".*I love (.*)": [
        "Tell me more about why you love {}.",
        "What do you enjoy most about {}?",
        "How does {} make you feel?",
        "How long have you loved {}?",
        "Does loving {} bring you joy?",
        "How do others respond to your love for {}?",
        "Has loving {} changed over time?",
        "What do you wish others understood about your love for {}?",
        "How do you express your love for {}?",
        "What does loving {} mean to you?",
    ],
    # Additions for love life, breakup, family issues, and academic struggles
    r".*I am having trouble with my love life (.*)": [
        "What do you think is causing trouble in your love life?",
        "How has this affected your feelings?",
        "Do you feel your love life is improving or worsening?",
    ],
    r".*I just had a breakup (.*)": [
        "I'm sorry to hear about your breakup. How are you feeling?",
        "Breakups can be tough. What’s been the hardest part for you?",
        "What have you been doing to cope after the breakup?",
    ],
    r".*my parents are divorced (.*)": [
        "How has your parents' divorce affected you?",
        "Do you feel different since the divorce?",
        "What do you think about your relationship with each parent now?",
    ],
    r".*my pet died (.*)": [
        "I'm really sorry about your loss. How are you feeling about your pet’s passing?",
        "Losing a pet can be so hard. What’s your favorite memory with your pet?",
        "How are you coping with the loss of your pet?",
    ],
    r".*my mom died (.*)": [
        "I'm really sorry for your loss. How are you coping with your mother’s passing?",
        "Losing a parent is incredibly hard. How are you feeling?",
        "What are your thoughts when you think about your mom?",
    ],
    r".*my dad died (.*)": [
        "I'm really sorry to hear that. How are you dealing with your dad’s death?",
        "How has your life changed since your dad passed away?",
        "Do you have someone you can talk to about losing your dad?",
    ],
    r".*I got a low score in my exams (.*)": [
        "Why do you think you got a low score?",
        "What can you do differently to improve your score next time?",
        "How did getting a low score make you feel?",
    ],
    r".*I am not performing well in college (.*)": [
        "What do you think is affecting your performance in college?",
        "How do you feel about your current academic performance?",
        "What steps can you take to improve your performance?",
    ],
    r".*I am not doing well in school (.*)": [
        "What has been making it difficult for you to do well in school?",
        "Do you feel overwhelmed by school?",
        "What changes do you think would help you perform better?",
    ],
    r".*I am having trouble keeping up with my studies (.*)": [
        "What’s been the biggest challenge in keeping up with your studies?",
        "How does falling behind in studies make you feel?",
        "What strategies have you tried to keep up with your studies?",
    ],
    r".*I am spending too much time on games (.*)": [
        "Why do you think you’re spending so much time on games?",
        "How does gaming impact your other responsibilities?",
        "What can you do to balance your gaming with other activities?",
    ],
    r".*I feel anxious about (.*)": [
        "What specifically makes you anxious about {}?",
        "How do you usually deal with anxiety related to {}?",
        "Has your anxiety about {} increased recently?",
        "What helps to calm your anxiety about {}?",
    ],
    r".*I feel depressed about (.*)": [
        "I'm really sorry you're feeling this way. What do you think contributes to feeling depressed about {}?",
        "When did you start feeling depressed about {}?",
        "Have you been able to talk to anyone about your depression?",
        "What helps you cope when you feel depressed about {}?",
    ],
    r".*I lack motivation (.*)": [
        "Why do you think you’re struggling with motivation?",
        "What usually helps boost your motivation?",
        "Has your lack of motivation been affecting your goals?",
        "What’s been causing you to feel demotivated?",
    ],
    r".*I don't like how I look (.*)": [
        "Why do you feel unhappy about how you look?",
        "Have you always felt this way about your appearance?",
        "What could help you feel more comfortable with how you look?",
        "Do you feel pressure to look a certain way?",
    ],
    r"I don't have many friends": [
        "Why do you feel like you don’t have many friends?",
        "Has it always been difficult for you to make friends?",
        "What makes it hard to connect with others?",
        "What qualities do you value in a friend?",
    ],
    r"I feel lonely": [
        "Why do you think you feel lonely?",
        "Has loneliness been affecting your mood?",
        "What usually helps when you feel lonely?",
        "Do you think reaching out to someone would help?",
    ],
    r"I am worried about my career": [
        "What aspect of your career worries you the most?",
        "Do you feel prepared for your career challenges?",
        "What do you think would ease your career-related stress?",
        "How do you plan to manage your career worries?",
    ],
    r"I don't feel good enough": [
        "What makes you feel like you’re not good enough?",
        "Has this feeling been constant, or is it triggered by something?",
        "What would help you feel more confident in your abilities?",
        "Have you experienced success in the past that contradicts this feeling?",
    ],
    r".*i feel overwhelmed (.*)": [
        "what’s making you feel overwhelmed by {}?",
        "when did you start feeling overwhelmed?",
        "how do you usually deal with feeling overwhelmed?",
        "have you tried breaking tasks down to manage the feeling?",
    ],
    r".*i don’t know what to do (.*)": [
        "what makes you feel unsure about what to do?",
        "have you considered seeking advice from someone?",
        "do you feel stuck because of too many options or too few?",
        "what would help you find clarity on what to do?",
    ],
    r".*i feel lost (.*)": [
        "why do you feel lost when it comes to {}?",
        "what do you think would help you find direction?",
        "have you felt this way before?",
        "what usually helps you feel less lost?",
    ],
    r".*i don’t feel like myself (.*)": [
        "can you explain what makes you feel different from yourself?",
        "when did you start feeling like you’re not yourself?",
        "have you noticed any changes in your routine?",
        "what do you think could bring you back to feeling like yourself?",
    ],
    r".*i feel stuck (.*)": [
        "what do you think is causing you to feel stuck with {}?",
        "do you feel stuck because of external factors or internal ones?",
        "what small steps can you take to move forward?",
        "how do you usually overcome the feeling of being stuck?",
    ],
    r".*i can’t focus (.*)": [
        "what's distracting you from focusing on {}?",
        "has something changed recently that’s affecting your focus?",
        "what techniques have helped you improve your focus in the past?",
        "how does not being able to focus make you feel?",
    ],
    r".*i feel anxious around people (.*)": [
        "what do you think causes your anxiety around people?",
        "have you always felt anxious in social settings?",
        "what helps you manage your social anxiety?",
        "would you like to improve how you feel in social situations?",
    ],
    r".*i don’t trust anyone (.*)": [
        "what makes it difficult for you to trust others?",
        "have past experiences influenced your lack of trust?",
        "do you want to rebuild trust in people?",
        "how does not trusting anyone affect your relationships?",
    ],
    r".*i have too much on my plate (.*)": [
        "what are the main things contributing to your load?",
        "is there anything you can delegate or postpone?",
        "how does having too much on your plate make you feel?",
        "what can you do to lighten your load?",
    ],
    r".*i am constantly tired (.*)": [
        "why do you think you’re always feeling tired?",
        "have you noticed patterns that make you feel more tired?",
        "are there lifestyle changes you could make to improve your energy?",
        "how does feeling tired impact your day-to-day life?",
    ],
    r".*i am afraid of change (.*)": [
        "what specifically about change makes you afraid?",
        "how has fear of change impacted your decisions?",
        "do you think embracing change could be positive for you?",
        "have you experienced positive changes before?",
    ],
    r".*i procrastinate a lot (.*)": [
        "why do you think you procrastinate on {}?",
        "what usually triggers your procrastination?",
        "how do you feel when you procrastinate?",
        "what helps you overcome procrastination?",
    ],
    r".*i feel like a burden (.*)": [
        "why do you think you’re a burden to others?",
        "have others made you feel this way, or is it internal?",
        "what would help you stop feeling like a burden?",
        "how do you feel about asking for help when needed?",
    ],
    r".*i feel disconnected from others (.*)": [
        "what makes you feel disconnected from others?",
        "have you tried reaching out to people around you?",
        "how does feeling disconnected affect your mood?",
        "what could help you feel more connected?",
    ],
    r".*i’m afraid to fail (.*)": [
        "what does failure represent for you?",
        "has fear of failure stopped you from pursuing goals?",
        "what would help you manage your fear of failure?",
        "how would you define success for yourself?",
    ],
    r".*i feel guilty (.*)": [
        "why do you think you feel guilty about {}?",
        "has this guilt been affecting your mood?",
        "is there anything you can do to address the source of your guilt?",
        "do you find it hard to forgive yourself?",
    ],
    r".*i feel worthless (.*)": [
        "why do you feel worthless about {}?",
        "what would help you feel more valuable?",
        "have others contributed to this feeling?",
        "what qualities about yourself do you appreciate?",
    ],
    r".*i’m struggling to be consistent (.*)": [
        "what makes it hard for you to maintain consistency?",
        "how do you feel when you’re not consistent?",
        "what tools or techniques could help improve your consistency?",
        "is there something specific that disrupts your consistency?",
    ],
    r".*i’m feeling emotionally drained (.*)": [
        "what’s been draining your emotions lately?",
        "how do you usually recharge when feeling emotionally drained?",
        "do you think external pressures are contributing to this?",
        "how has being emotionally drained impacted your daily life?",
    ],
    r".*i have trouble setting boundaries (.*)": [
        "why do you think it’s hard for you to set boundaries?",
        "how do you feel when you fail to set a boundary?",
        "what could help you feel more confident in setting boundaries?",
        "have you had positive experiences with boundaries in the past?",
    ],
    r".*i feel like giving up (.*)": [
        "what’s making you feel like giving up?",
        "have you faced similar challenges before?",
        "what usually helps you push through when things get tough?",
        "is there someone who can support you through this?",
    ],
    r".*i feel inadequate (.*)": [
        "why do you feel inadequate about {}?",
        "what would help you feel more capable?",
        "is this feeling of inadequacy connected to external factors?",
        "have you accomplished things in the past that contradict this feeling?",
    ],
    r".*i’m scared of the future (.*)": [
        "what about the future scares you?",
        "how do you usually cope with uncertainty?",
        "is there anything that gives you hope for the future?",
        "how can you manage your fear of the unknown?",
    ],
    r".*i can’t handle criticism (.*)": [
        "why do you think criticism is hard for you to handle?",
        "how does receiving criticism make you feel?",
        "is there a way to reframe criticism as constructive?",
        "what could help you take criticism more positively?",
    ],
    r".*i feel left out (.*)": [
        "why do you think you feel left out?",
        "have you tried sharing these feelings with others?",
        "how does feeling left out affect your self-esteem?",
        "what could help you feel more included?",
    ],
    r".*i’m scared to speak up (.*)": [
        "what makes you afraid to speak up?",
        "have you had negative experiences when speaking up?",
        "what could help you feel more confident in sharing your thoughts?",
        "is there a safe space where you feel comfortable speaking up?",
    ],
    r".*i feel hopeless (.*)": [
        "why do you think you’re feeling hopeless about {}?",
        "what has contributed to this sense of hopelessness?",
        "is there anything that could reignite hope for you?",
        "have you felt this way before and overcome it?",
    ],
    r".*i’m always worried (.*)": [
        "what do you think triggers your constant worry?",
        "have you tried any strategies to manage your worry?",
        "how does worrying so much affect your life?",
        "what would ease your constant worry?",
    ],
    r".*i can’t sleep (.*)": [
        "what do you think is affecting your ability to sleep?",
        "have you experienced changes in your routine that impact your sleep?",
        "what usually helps you fall asleep when you’re struggling?",
        "how does not sleeping affect your mood and energy levels?",
    ],
    r".*i feel misunderstood (.*)": [
        "what makes you feel misunderstood?",
        "have you tried expressing your feelings to others?",
        "how does being misunderstood impact your relationships?",
        "what would help you feel more understood?",
    ],
    r".*i don’t like confrontation (.*)": [
        "what about confrontation makes you uncomfortable?",
        "have you always felt uneasy about confrontation?",
        "how does avoiding confrontation impact your interactions?",
        "what would help you feel more confident in handling conflict?",
    ],
    r".*i feel judged (.*)": [
        "why do you feel judged by others?",
        "have you experienced situations where you felt judged?",
        "how does feeling judged impact your behavior?",
        "what would help you feel less judged?",
    ],
    r".*i’m afraid of rejection (.*)": [
        "why does rejection feel scary for you?",
        "have you experienced rejection in the past that impacted you?",
        "what would help you manage your fear of rejection?",
        "how do you cope when faced with the possibility of rejection?",
    ],
    r".*i don’t feel confident (.*)": [
        "what do you think is affecting your confidence?",
        "have you experienced periods where you felt more confident?",
        "what could help you build your confidence?",
        "how does a lack of confidence affect your day-to-day life?",
    ],
    r".*i don’t know what i want (.*)": [
        "what makes you feel uncertain about what you want?",
        "have you considered different options to help clarify your desires?",
        "what usually helps you when you feel indecisive?",
        "what could help you gain more clarity on what you want?",
    ],
    r".*i feel insecure (.*)": [
        "why do you think you’re feeling insecure about {}?",
        "has something triggered your feelings of insecurity?",
        "what would help you feel more secure in yourself?",
        "how do you usually manage feelings of insecurity?",
    ],
    r".*i feel like i’m failing (.*)": [
        "why do you feel like you’re failing at {}?",
        "has this feeling of failure been ongoing?",
        "what could help you change your perspective on this?",
        "have you had successes that contradict this feeling?",
    ],
    r".*i’m not good at (.*)": [
        "why do you feel like you’re not good at {}?",
        "is there something specific that makes you doubt your ability?",
        "what could help you improve at {}?",
        "have you sought feedback or guidance on {}?",
    ],
    r".*i feel helpless (.*)": [
        "what is making you feel helpless about {}?",
        "how does feeling helpless affect your outlook?",
        "is there someone you can reach out to for support?",
        "what could help you feel more in control?",
    ],
    r".*i can’t make decisions (.*)": [
        "what makes it hard for you to make decisions?",
        "have you tried weighing the pros and cons of your choices?",
        "what usually helps you decide when you feel stuck?",
        "what could make decision-making less stressful for you?",
    ],
    r".*i feel overwhelmed by choices (.*)": [
        "what about having so many choices makes you feel overwhelmed?",
        "how do you usually narrow down your options?",
        "have you tried prioritizing what matters most to you?",
        "what would help you feel less overwhelmed by the choices?",
    ],
    r".*i don’t know how to relax (.*)": [
        "why do you think it’s hard for you to relax?",
        "what usually helps you feel calmer?",
        "have you tried any relaxation techniques?",
        "how do you feel when you try to relax but can’t?",
    ],
    r".*i feel anxious about the future (.*)": [
        "what specific part of the future makes you anxious?",
        "have you tried focusing on what you can control?",
        "how does this anxiety affect your present moment?",
        "what could help ease your future-related anxiety?",
    ],
    r".*i feel stuck in my career (.*)": [
        "what makes you feel stuck in your career?",
        "have you considered exploring new opportunities?",
        "how does feeling stuck impact your job satisfaction?",
        "what would help you feel more fulfilled in your career?",
    ],
    r".*i don’t feel supported (.*)": [
        "why do you feel like you’re not being supported?",
        "have you shared these feelings with those close to you?",
        "what kind of support do you think would help?",
        "how does not feeling supported affect your well-being?",
    ],
    r".*i feel unmotivated (.*)": [
        "What do you think is causing your lack of motivation?",
        "Have you set any small goals to help you get started?",
        "What activities inspire you or bring you joy?",
        "How about creating a reward system for yourself?",
    ],
    r".*i want to improve my life (.*)": [
        "What specific areas do you want to improve?",
        "Have you thought about taking small steps toward your goals?",
        "What does a better life look like for you?",
        "How can you celebrate your progress along the way?",
    ],
    r".*i feel unmotivated (.*)": [
        "What do you think is causing your lack of motivation?",
        "Have you set any small goals to help you get started?",
        "What activities inspire you or bring you joy?",
        "How about creating a reward system for yourself?",
    ],
    r".*i want to improve my life (.*)": [
        "What specific areas do you want to improve?",
        "Have you thought about taking small steps toward your goals?",
        "What does a better life look like for you?",
        "How can you celebrate your progress along the way?",
    ],
    r".*i’m feeling lost (.*)": [
        "What aspects of your life do you feel lost in?",
        "Have you considered talking to someone about these feelings?",
        "What activities make you feel more grounded?",
        "How can you give yourself permission to explore new paths?",
    ],
    r".*i need a change (.*)": [
        "What kind of change are you hoping for?",
        "Have you thought about trying something new?",
        "What steps can you take to initiate this change?",
        "How do you think a change would benefit you?",
    ],
    r".*i feel like giving up (.*)": [
        "What makes you feel like giving up?",
        "Have you thought about what you've already accomplished?",
        "What would you say to a friend in your situation?",
        "How can you break your challenges into smaller, manageable parts?",
    ],
    r".*i want to be happier (.*)": [
        "What does happiness mean to you?",
        "Have you identified activities that bring you joy?",
        "How can you incorporate more joy into your daily routine?",
        "What small changes can you make to improve your mood?",
    ],
    r".*i’m afraid of failure (.*)": [
        "What does failure mean to you?",
        "Have you considered the lessons that can come from failure?",
        "How can you reframe your view of failure as a learning opportunity?",
        "What steps can you take to prepare for challenges ahead?",
    ],
    r".*i want to be more productive (.*)": [
        "What specific tasks do you want to be more productive with?",
        "Have you tried setting a daily schedule or to-do list?",
        "What time of day do you feel most productive?",
        "How can you minimize distractions while working?",
    ],
    r".*i’m feeling overwhelmed (.*)": [
        "What specifically is making you feel overwhelmed?",
        "Have you tried breaking tasks into smaller steps?",
        "How does taking a break make you feel?",
        "What relaxation techniques have you found helpful?",
    ],
    r".*i need support (.*)": [
        "What kind of support are you looking for?",
        "Have you reached out to friends or family for help?",
        "What resources are available to you right now?",
        "How can you build a support network around you?",
    ],
    r".*i want to achieve my goals (.*)": [
        "What specific goals do you want to achieve?",
        "Have you created a plan to reach these goals?",
        "What motivates you to pursue these goals?",
        "How can you celebrate your achievements, big or small?",
    ],
    r".*i’m feeling anxious (.*)": [
        "What triggers your anxiety most often?",
        "Have you tried deep breathing or mindfulness techniques?",
        "How does talking about your anxiety make you feel?",
        "What coping strategies have worked for you in the past?",
    ],
    r".*i feel like i’m not enough (.*)": [
        "What makes you feel that way?",
        "Have you considered the things you are proud of?",
        "How can you practice self-compassion?",
        "What would you tell a friend who feels this way?",
    ],
    r".*i want to learn something new (.*)": [
        "What topic interests you the most?",
        "Have you found any resources or classes you’d like to try?",
        "How can you dedicate time each week to learning?",
        "What small steps can you take to start this journey?",
    ],
    r".*i’m struggling with self-doubt (.*)": [
        "What situations trigger your self-doubt?",
        "How can you remind yourself of your strengths?",
        "Have you thought about keeping a journal of your achievements?",
        "What would you do if you weren't afraid of failing?",
    ],
    r".*i want to build better habits (.*)": [
        "What habits do you want to build?",
        "Have you considered starting with one small change?",
        "How can you track your progress?",
        "What rewards can you give yourself for sticking to your habits?",
    ],
    r".*i feel disconnected (.*)": [
        "What makes you feel disconnected?",
        "Have you reached out to friends or family recently?",
        "What activities help you feel more connected?",
        "How can you create opportunities for social interaction?",
    ],
    r".*i’m not happy with my job (.*)": [
        "What specifically about your job makes you unhappy?",
        "Have you thought about what would make it better?",
        "What are your career goals moving forward?",
        "How can you explore new opportunities?",
    ],
    r".*i feel like i don’t belong (.*)": [
        "What experiences contribute to this feeling?",
        "Have you considered finding communities that align with your interests?",
        "What makes you feel connected to others?",
        "How can you engage in activities that make you feel included?",
    ],
    r".*i need to take care of myself (.*)": [
        "What self-care activities do you enjoy?",
        "How can you prioritize self-care in your routine?",
        "What small changes can you make to care for your mental health?",
        "How do you feel when you take time for yourself?",
    ],
    r".*i want to express my feelings (.*)": [
        "What emotions are you struggling to express?",
        "Have you thought about journaling or talking to someone?",
        "How does expressing your feelings help you?",
        "What would it look like to share your feelings with others?",
    ],
    r".*i’m feeling stagnant (.*)": [
        "What aspects of your life feel stagnant right now?",
        "Have you considered trying something new to shake things up?",
        "What steps can you take to move forward?",
        "How can you challenge yourself to grow?",
    ],
    r".*i want to build my confidence (.*)": [
        "What situations make you feel less confident?",
        "Have you celebrated your small successes?",
        "How can you practice self-affirmation?",
        "What would help you feel more confident in your abilities?",
    ],
    r".*i’m struggling with change (.*)": [
        "What changes are you finding difficult?",
        "Have you thought about the positives that can come from change?",
        "What strategies can help you adapt?",
        "How can you give yourself grace during this transition?",
    ],
    r".*i need to be more patient (.*)": [
        "What situations test your patience the most?",
        "Have you considered practicing mindfulness to help?",
        "How do you feel when you are patient with yourself?",
        "What small steps can you take to cultivate patience?",
    ],
    r".*i want to find balance in my life (.*)": [
        "What areas of your life feel out of balance?",
        "Have you tried setting boundaries in your activities?",
        "How can you create a routine that feels more balanced?",
        "What makes you feel centered and grounded?",
    ],
    r".*i’m looking for purpose (.*)": [
        "What gives your life meaning?",
        "Have you thought about what you’re passionate about?",
        "How can you explore new interests to find your purpose?",
        "What activities make you feel fulfilled?",
    ],
    r".*i want to build resilience (.*)": [
        "What challenges have you faced that tested your resilience?",
        "Have you considered how you can learn from past experiences?",
        "What strategies help you cope with adversity?",
        "How can you reframe setbacks as opportunities for growth?",
    ],
    r".*i feel like i’m in a rut (.*)": [
        "What aspects of your life contribute to this feeling?",
        "Have you tried shaking up your routine?",
        "What new activities could you explore?",
        "How can you reconnect with your passions?",
    ],
    r".*i want to surround myself with positivity (.*)": [
        "What influences your current environment?",
        "Have you considered distancing yourself from negativity?",
        "What positive affirmations resonate with you?",
        "How can you cultivate an uplifting atmosphere?",
    ],
    r".*i’m seeking clarity (.*)": [
        "What areas of your life feel unclear?",
        "Have you considered writing down your thoughts?",
        "What can help you gain perspective on your situation?",
        "How does talking things out with someone help?",
    ],
    r".*i need to forgive myself (.*)": [
        "What do you need to forgive yourself for?",
        "How has holding onto guilt affected you?",
        "What steps can you take toward self-forgiveness?",
        "How can you practice compassion for yourself?",
    ],
    r".*i feel unmotivated (.*)": [
        "It’s completely normal to feel unmotivated at times. What do you think is causing this feeling?",
        "Sometimes a lack of motivation can stem from feeling overwhelmed. Have you considered setting smaller goals to help you get started?",
        "When you feel unmotivated, what activities inspire you or bring you joy? Perhaps re-engaging with those can help lift your spirits.",
        "Creating a reward system for yourself might be beneficial. What would motivate you to take those first steps?",
    ],
    r".*i want to improve my life (.*)": [
        "Improving your life is a commendable goal. What specific areas are you looking to enhance?",
        "Have you thought about taking small, actionable steps toward your goals? Sometimes, gradual changes can lead to significant improvements.",
        "What does a better life look like for you? Visualizing your goals can often provide clarity on the steps needed to achieve them.",
        "Celebrating your progress, no matter how small, is important. How can you acknowledge the improvements you make along the way?",
    ],
    r".*i’m feeling lost (.*)": [
        "Feeling lost can be quite challenging. What aspects of your life do you feel most uncertain about right now?",
        "Talking to someone about these feelings can sometimes provide new perspectives. Have you considered reaching out for support?",
        "Engaging in activities that make you feel more grounded could help. What are some things you enjoy doing that bring you a sense of stability?",
        "It's okay to explore new paths and give yourself permission to change direction. What steps can you take to begin this exploration?",
    ],
    r".*i need a change (.*)": [
        "Change can be a vital part of growth. What kind of change are you hoping to achieve in your life?",
        "Trying something new can often lead to exciting opportunities. Have you thought about what steps you can take to initiate this change?",
        "Identifying what aspects of your life you want to change can be empowering. How do you think a change would benefit you personally?",
        "Consider the potential positives that could arise from making a change. How might your life look different as a result?",
    ],
    r".*i feel like giving up (.*)": [
        "It’s tough to feel like giving up, but it’s important to remember that you’ve already come so far. What makes you feel this way right now?",
        "Reflecting on what you’ve accomplished so far can be motivating. Have you considered how you can break your challenges into smaller, more manageable parts?",
        "If a friend were in your position, what would you say to encourage them? Sometimes, viewing your situation from an outsider's perspective can help.",
        "Think about what small steps you can take to regain your motivation. What is one thing you could do today that might help you feel better?",
    ],
    r".*i want to be happier (.*)": [
        "Happiness is something we all strive for. What does happiness mean to you personally?",
        "Identifying activities that bring you joy is a great step. Have you considered incorporating more of those into your daily routine?",
        "Making small changes to improve your mood can have a big impact over time. What are some things you can do to boost your happiness?",
        "Reflecting on what makes you feel content can guide you toward a happier life. What are some moments that have brought you joy recently?",
    ],
    r".*i’m afraid of failure (.*)": [
        "Fear of failure is a common experience, but it can also be a learning opportunity. What does failure mean to you?",
        "Reframing your view of failure can help. How can you see it as a stepping stone to growth rather than a setback?",
        "Preparation can often reduce the fear of failure. What steps can you take to feel more ready to face challenges ahead?",
        "Think about the lessons you've learned from past failures. How might these experiences help you in the future?",
    ],
    r".*i want to be more productive (.*)": [
        "Boosting your productivity is a worthwhile goal. What specific tasks are you hoping to improve upon?",
        "Creating a daily schedule or to-do list can help you stay organized. Have you tried setting clear priorities for your tasks?",
        "Recognizing the times of day when you feel most productive can help you schedule your most important work during those periods. What times work best for you?",
        "Minimizing distractions is crucial for productivity. What changes can you make to your environment to enhance your focus?",
    ],
    r".*i’m feeling overwhelmed (.*)": [
        "Feeling overwhelmed can be quite difficult to manage. What specific factors are contributing to this feeling?",
        "Breaking tasks into smaller steps can often alleviate feelings of overwhelm. Have you tried this approach before?",
        "Taking a break to recharge can make a significant difference. How does giving yourself some time to relax make you feel?",
        "Consider what relaxation techniques have worked for you in the past. What strategies can you implement now to help manage your stress?",
    ],
    r".*i need support (.*)": [
        "Seeking support is a brave step. What kind of support are you currently looking for?",
        "Reaching out to friends or family can often provide comfort. Have you considered talking to someone you trust about how you feel?",
        "There are many resources available to help you. What options do you think might be beneficial for you right now?",
        "Building a support network can be incredibly helpful. How can you engage with others to create that network?",
    ],
    r".*i want to achieve my goals (.*)": [
        "Setting goals is a powerful motivator. What specific goals are you aiming to achieve?",
        "Creating a structured plan can guide you toward these goals. Have you taken the time to outline the steps you need to take?",
        "What motivates you to pursue these goals? Understanding your 'why' can strengthen your commitment.",
        "Celebrating your achievements, no matter how small, is essential. How do you plan to acknowledge your progress?",
    ],
    r".*i feel stuck (.*)": [
        "Feeling stuck can be incredibly frustrating. What areas of your life do you feel particularly stagnant in right now?",
        "Sometimes, a change in perspective can help you see new options. Have you thought about seeking advice from someone who might offer a different viewpoint?",
        "Identifying what is keeping you from moving forward is a crucial step. Can you pinpoint any specific barriers that you believe are holding you back?",
        "It might help to write down your feelings and thoughts. What insights can you gain from reflecting on your situation in that way?",
    ],
    r".*i want to build better habits (.*)": [
        "Building better habits is a fantastic goal. What specific habits are you looking to develop or improve?",
        "Starting small can often lead to lasting change. What is one tiny habit you can commit to today that aligns with your goals?",
        "Tracking your progress can provide motivation. How do you plan to measure your success as you work on these new habits?",
        "Consider the reasons behind wanting to build these habits. How do you believe they will enhance your life in the long run?",
    ],
    r".*i’m feeling anxious (.*)": [
        "Anxiety can be overwhelming, but acknowledging it is an important first step. What triggers your anxiety the most?",
        "Practicing mindfulness or deep breathing can sometimes help ease anxiety. Have you tried any relaxation techniques that work for you?",
        "It’s okay to seek professional help if your anxiety feels unmanageable. What resources have you considered exploring?",
        "Sharing your feelings with someone you trust can provide relief. Who in your life do you feel comfortable talking to about your anxiety?",
    ],
    r".*i feel lonely (.*)": [
        "Loneliness can be difficult to navigate. What situations or moments amplify your feelings of loneliness?",
        "Engaging in community activities or hobbies can often help you connect with others. What interests do you have that might allow you to meet new people?",
        "Reaching out to old friends or family members can help combat loneliness. Is there someone you’ve been wanting to reconnect with?",
        "It’s essential to remember that feeling lonely is a common experience. How can you practice self-compassion during these times?",
    ],
    r".*i want to develop self-confidence (.*)": [
        "Developing self-confidence is a valuable pursuit. What specific areas do you feel you lack confidence in?",
        "Setting small, achievable goals can boost your confidence over time. What is one goal you can set for yourself this week?",
        "Positive affirmations can help reshape your self-perception. What affirmations can you repeat to yourself to foster confidence?",
        "Surrounding yourself with supportive people can make a significant difference. Who in your life uplifts you and encourages your growth?",
    ],
    r".*i’m having trouble with my self-esteem (.*)": [
        "Struggling with self-esteem is something many people experience. What are the main thoughts that contribute to your feelings of low self-worth?",
        "Engaging in activities that showcase your strengths can help improve self-esteem. What are some of your skills or talents that you take pride in?",
        "Challenging negative self-talk is crucial. What strategies can you use to counter those negative thoughts when they arise?",
        "Consider reflecting on your past achievements, no matter how small. What successes can you remind yourself of to boost your confidence?",
    ],
    r".*i want to find my passion (.*)": [
        "Finding your passion can be a transformative journey. What activities make you lose track of time or bring you immense joy?",
        "Experimenting with different hobbies and interests can help you discover what you truly love. What new activities have you thought about trying?",
        "Talking to others about their passions can spark inspiration. Have you reached out to friends or mentors to learn about what drives them?",
        "Reflecting on your values and what matters most to you can guide you toward your passion. What do you feel most strongly about in life?",
    ],
    r".*i’m feeling overwhelmed with choices (.*)": [
        "Having too many choices can indeed be overwhelming. What decisions are you currently facing that feel particularly daunting?",
        "Breaking down your options into pros and cons can help clarify your thoughts. Have you considered making a list to visualize your choices?",
        "Sometimes, taking a step back and giving yourself a break can provide clarity. What can you do to give yourself some mental space?",
        "Trusting your intuition can also be helpful. How do you usually feel when you think about each option? Does one feel more aligned with you?",
    ],
    r".*i want to enhance my creativity (.*)": [
        "Enhancing creativity is a wonderful goal. What areas of your life would you like to apply more creativity to?",
        "Engaging in creative activities regularly can help stimulate your imagination. What artistic hobbies have you considered exploring?",
        "Surrounding yourself with inspiring content, like books, art, or music, can also boost your creativity. What inspires you the most?",
        "Don’t be afraid to take risks in your creative endeavors. What is one unconventional idea you have that you could experiment with?",
    ],
    r".*i feel disconnected from my goals (.*)": [
        "Feeling disconnected from your goals can be disheartening. What specific goals do you feel less connected to at the moment?",
        "Reflecting on your reasons for setting those goals can reignite your passion. What motivated you to pursue them in the first place?",
        "Sometimes, revisiting and adjusting your goals can create a stronger connection. What changes could you make to align them more with your current values?",
        "Consider creating a vision board to visualize your goals and dreams. How might this help you reconnect with your aspirations?",
    ],
    r".*i want to manage my time better (.*)": [
        "Time management is essential for productivity. What specific areas of your life do you feel you need to manage your time more effectively?",
        "Creating a structured schedule can provide clarity. Have you tried planning your day or week in advance to prioritize tasks?",
        "Setting boundaries on distractions can greatly enhance focus. What changes can you make to your environment to help minimize interruptions?",
        "Reflecting on how you currently spend your time can highlight areas for improvement. What insights can you gather from tracking your daily activities?",
    ],
    r".*i want to improve my relationships (.*)": [
        "Improving relationships is a commendable goal. What specific relationships are you looking to enhance?",
        "Effective communication is key in any relationship. Have you considered discussing your feelings openly with those you care about?",
        "Investing quality time with loved ones can strengthen bonds. What activities can you do together to foster connection and understanding?",
        "Reflecting on past experiences in your relationships can provide valuable lessons. What have you learned that you can apply moving forward?",
    ],
    r".*i feel unappreciated (.*)": [
        "Feeling unappreciated can be disheartening. In what areas of your life do you feel this lack of recognition the most?",
        "Openly expressing your feelings to those around you can sometimes lead to positive change. Have you considered sharing how you feel with others?",
        "Finding ways to acknowledge your own achievements is also essential. What can you do to celebrate your efforts and successes, even if others don't recognize them?",
        "Surrounding yourself with supportive individuals who value you can make a significant difference. Who in your life uplifts you and recognizes your worth?",
    ],
    r".*i'm worried about my mental health (.*)": [
        "It's completely understandable to feel worried about your mental health. Talking to a trusted friend or family member can help provide support and perspective. Have you thought about reaching out to someone you feel comfortable with?",
        "Seeking professional help is an important step if you're feeling concerned. A mental health professional can offer guidance tailored to your specific needs. What steps can you take to find someone who can support you?",
        "Educating yourself about mental health can be empowering. Understanding your feelings and the factors that contribute to them can help you feel more in control. What resources or books might you explore to gain more insight?",
        "Prioritizing self-care is essential. Engaging in activities that bring you joy and relaxation can help improve your overall well-being. What hobbies or activities make you feel most relaxed and fulfilled?",
        "It’s crucial to recognize that it’s okay to seek help; it's a sign of strength, not weakness. How can you practice self-compassion as you navigate these feelings?",
    ],
    r".*i feel overwhelmed (.*)": [
        "Feeling overwhelmed can happen to anyone, and it's important to take a moment to breathe and ground yourself. Have you tried deep breathing exercises or mindfulness techniques to help manage that feeling?",
        "Breaking tasks into smaller, manageable steps can help reduce feelings of overwhelm. What are some tasks you can prioritize or break down to make them feel less daunting?",
        "Identifying your triggers can empower you to address them more effectively. What specific situations or responsibilities are contributing to your sense of overwhelm?",
        "Consider giving yourself permission to take breaks. Taking short pauses can rejuvenate your mind and body. How can you incorporate more downtime into your routine?",
    ],
    r".*i want to improve my self-esteem (.*)": [
        "Improving self-esteem is a valuable journey. Reflecting on your strengths and achievements can help you appreciate your worth. What are some accomplishments you're proud of, no matter how small?",
        "Challenging negative self-talk is essential for building self-esteem. What are some affirmations you can repeat to yourself to reinforce positive beliefs about yourself?",
        "Surrounding yourself with supportive individuals can significantly enhance your self-image. Who in your life makes you feel valued and appreciated?",
        "Engaging in activities that allow you to express yourself can also boost your confidence. What creative outlets or hobbies can you explore to showcase your talents?",
    ],
    r".*i feel disconnected from others (.*)": [
        "Feeling disconnected can be tough, but it's important to remember that you're not alone. What steps can you take to reach out and connect with those you care about?",
        "Engaging in community activities or joining clubs related to your interests can foster connections. What hobbies or passions can you pursue to meet like-minded people?",
        "Sometimes, sharing your feelings with someone can bridge the gap of disconnection. Is there someone you trust that you could talk to about how you're feeling?",
        "Practicing empathy and understanding can enhance relationships. How can you show support and kindness to those around you to strengthen your connections?",
    ],
    r".*i want to manage my anxiety better (.*)": [
        "Managing anxiety is a journey, and it's commendable that you want to work on it. Have you explored mindfulness practices or meditation techniques that can help calm your mind?",
        "Identifying your anxiety triggers can empower you to cope more effectively. What situations or thoughts tend to heighten your anxiety, and how can you prepare for them?",
        "Establishing a routine that includes physical activity can be beneficial for managing anxiety. What forms of exercise do you enjoy, and how can you incorporate them into your week?",
        "Consider developing a toolkit of coping strategies that you can use when anxiety arises. What techniques have you found helpful in the past that you can rely on?",
    ],
    r".*i feel sad often (.*)": [
        "Feeling sad is a natural part of life, but it’s important to address those feelings. Have you taken some time to reflect on what might be contributing to your sadness?",
        "Connecting with friends or family and sharing your feelings can provide comfort and understanding. Who in your life can you talk to when you're feeling down?",
        "Engaging in activities that you enjoy can help uplift your mood. What hobbies or interests can you pursue to bring a sense of joy back into your life?",
        "Practicing gratitude can also shift your perspective. What are some things, no matter how small, that you're grateful for today?",
    ],
    r".*i want to set goals for myself (.*)": [
        "Setting goals is a powerful way to create direction in your life. What specific areas would you like to focus on in your goal-setting journey?",
        "Breaking larger goals into smaller, achievable steps can make them feel more manageable. What is one small goal you can set for yourself this week?",
        "Visualizing your goals can enhance motivation. Have you considered creating a vision board to help keep your aspirations in sight?",
        "Regularly reviewing your goals and adjusting them as needed can ensure they remain relevant. How often do you think you could check in on your progress?",
    ],
    r".*i'm worried about my mental health (.*)": [
        "It's completely understandable to feel worried about your mental health. Talking to a trusted friend or family member can help provide support and perspective. Have you thought about reaching out to someone you feel comfortable with?",
        "Seeking professional help is an important step if you're feeling concerned. A mental health professional can offer guidance tailored to your specific needs. What steps can you take to find someone who can support you?",
        "Educating yourself about mental health can be empowering. Understanding your feelings and the factors that contribute to them can help you feel more in control. What resources or books might you explore to gain more insight?",
        "Prioritizing self-care is essential. Engaging in activities that bring you joy and relaxation can help improve your overall well-being. What hobbies or activities make you feel most relaxed and fulfilled?",
        "It’s crucial to recognize that it’s okay to seek help; it's a sign of strength, not weakness. How can you practice self-compassion as you navigate these feelings?",
    ],
    r".*i feel overwhelmed (.*)": [
        "Feeling overwhelmed can happen to anyone, and it's important to take a moment to breathe and ground yourself. Have you tried deep breathing exercises or mindfulness techniques to help manage that feeling?",
        "Breaking tasks into smaller, manageable steps can help reduce feelings of overwhelm. What are some tasks you can prioritize or break down to make them feel less daunting?",
        "Identifying your triggers can empower you to address them more effectively. What specific situations or responsibilities are contributing to your sense of overwhelm?",
        "Consider giving yourself permission to take breaks. Taking short pauses can rejuvenate your mind and body. How can you incorporate more downtime into your routine?",
    ],
    r".*i want to improve my self-esteem (.*)": [
        "Improving self-esteem is a valuable journey. Reflecting on your strengths and achievements can help you appreciate your worth. What are some accomplishments you're proud of, no matter how small?",
        "Challenging negative self-talk is essential for building self-esteem. What are some affirmations you can repeat to yourself to reinforce positive beliefs about yourself?",
        "Surrounding yourself with supportive individuals can significantly enhance your self-image. Who in your life makes you feel valued and appreciated?",
        "Engaging in activities that allow you to express yourself can also boost your confidence. What creative outlets or hobbies can you explore to showcase your talents?",
    ],
    r".*i feel disconnected from others (.*)": [
        "Feeling disconnected can be tough, but it's important to remember that you're not alone. What steps can you take to reach out and connect with those you care about?",
        "Engaging in community activities or joining clubs related to your interests can foster connections. What hobbies or passions can you pursue to meet like-minded people?",
        "Sometimes, sharing your feelings with someone can bridge the gap of disconnection. Is there someone you trust that you could talk to about how you're feeling?",
        "Practicing empathy and understanding can enhance relationships. How can you show support and kindness to those around you to strengthen your connections?",
    ],
    r".*i want to manage my anxiety better (.*)": [
        "Managing anxiety is a journey, and it's commendable that you want to work on it. Have you explored mindfulness practices or meditation techniques that can help calm your mind?",
        "Identifying your anxiety triggers can empower you to cope more effectively. What situations or thoughts tend to heighten your anxiety, and how can you prepare for them?",
        "Establishing a routine that includes physical activity can be beneficial for managing anxiety. What forms of exercise do you enjoy, and how can you incorporate them into your week?",
        "Consider developing a toolkit of coping strategies that you can use when anxiety arises. What techniques have you found helpful in the past that you can rely on?",
    ],
    r".*i feel sad often (.*)": [
        "Feeling sad is a natural part of life, but it’s important to address those feelings. Have you taken some time to reflect on what might be contributing to your sadness?",
        "Connecting with friends or family and sharing your feelings can provide comfort and understanding. Who in your life can you talk to when you're feeling down?",
        "Engaging in activities that you enjoy can help uplift your mood. What hobbies or interests can you pursue to bring a sense of joy back into your life?",
        "Practicing gratitude can also shift your perspective. What are some things, no matter how small, that you're grateful for today?",
    ],
    r".*i want to set goals for myself (.*)": [
        "Setting goals is a powerful way to create direction in your life. What specific areas would you like to focus on in your goal-setting journey?",
        "Breaking larger goals into smaller, achievable steps can make them feel more manageable. What is one small goal you can set for yourself this week?",
        "Visualizing your goals can enhance motivation. Have you considered creating a vision board to help keep your aspirations in sight?",
        "Regularly reviewing your goals and adjusting them as needed can ensure they remain relevant. How often do you think you could check in on your progress?",
    ],
    r".*i feel stressed (.*)": [
        "Stress can feel overwhelming, but it's important to acknowledge it and take steps to manage it. Have you tried identifying specific stressors in your life so you can address them directly?",
        "Incorporating relaxation techniques into your routine, like yoga or meditation, can be incredibly beneficial. What activities do you enjoy that help you unwind?",
        "It's crucial to maintain a healthy work-life balance. How can you create boundaries to ensure you have time for yourself amidst your responsibilities?",
        "Consider keeping a journal to express your thoughts and feelings. Writing can be a therapeutic way to process stress and gain clarity. Have you ever tried journaling?",
    ],
    r".*i have negative thoughts (.*)": [
        "Negative thoughts can be challenging, but recognizing them is the first step toward change. Have you thought about how you can challenge these thoughts and replace them with more positive ones?",
        "Practicing mindfulness can help you observe negative thoughts without judgment. What mindfulness techniques can you incorporate into your daily routine?",
        "Surrounding yourself with positive influences can help shift your mindset. Are there people in your life who uplift you and encourage a more positive outlook?",
        "Creating a list of affirmations that resonate with you can help counter negative thoughts. What positive statements about yourself can you remind yourself of daily?",
    ],
    r".*i want to find purpose (.*)": [
        "Finding purpose can be a profound journey. Reflecting on your passions and values can guide you. What activities make you feel fulfilled and truly alive?",
        "Setting aside time for self-reflection can help you explore what matters most to you. Have you considered journaling about your values and goals?",
        "Engaging in volunteer work or community service can provide a sense of purpose. Are there causes that resonate with you that you could get involved with?",
        "Connecting with mentors or individuals who inspire you can provide insight and motivation. Who do you admire, and how can you learn from their experiences?",
    ],
    r".*i feel lonely (.*)": [
        "Loneliness is a common feeling, and it's important to reach out when you experience it. Have you thought about joining a group or class to meet new people?",
        "Sometimes, volunteering can help you connect with others while making a difference. What local organizations could you support to foster connections?",
        "Consider scheduling regular check-ins with friends or family, even if it's just a quick message or call. Who can you reach out to for support?",
        "Practicing self-compassion can help during lonely times. How can you show kindness to yourself as you navigate these feelings?",
    ],
    r".*i want to develop better coping strategies (.*)": [
        "Developing effective coping strategies is an important step toward managing your emotions. What are some techniques you've found helpful in the past?",
        "Consider exploring different relaxation methods, such as deep breathing, progressive muscle relaxation, or guided imagery. Which of these sounds appealing to you?",
        "Building a toolkit of coping mechanisms can empower you to handle stress better. What strategies can you add to your toolkit for when you need them most?",
        "Sometimes, seeking professional help can provide additional strategies and support. Have you considered talking to a therapist about your coping methods?",
    ],
    r".*i want to improve my relationships (.*)": [
        "Improving relationships often starts with open and honest communication. What steps can you take to express your feelings and needs to those you care about?",
        "Practicing active listening can enhance your connections. How can you show that you value others' perspectives in your conversations?",
        "Engaging in shared activities can strengthen bonds. What hobbies or interests can you explore together with friends or family to create lasting memories?",
        "Setting boundaries is also vital in relationships. How can you ensure your needs are met while still being supportive of others?",
    ],
    r".*i feel stuck (.*)": [
        "Feeling stuck can be frustrating, but it often signals an opportunity for growth. Have you taken some time to reflect on what areas of your life feel stagnant?",
        "Setting small, achievable goals can help you regain a sense of direction. What is one step you can take today to move forward in a positive way?",
        "Sometimes, a change of scenery can spark new inspiration. Have you thought about trying a new environment, like working in a different space or going for a walk in nature?",
        "Connecting with a mentor or someone who inspires you can provide new perspectives. Who in your life has overcome challenges that you admire?",
    ],
    r"how do i know if i’m unwell": [
        "If you're questioning your well-being, it's essential to reflect on various aspects of your mental and emotional state. Common indicators that you might be struggling include: 1. Persistent feelings of sadness or anxiety. 2. Not enjoying activities you once loved. 3. Changes in eating or sleeping habits. 4. Difficulty focusing or making decisions. 5. Constant fatigue or low energy. 6. Feelings of hopelessness or guilt. 7. Withdrawing from friends and family. 8. Increased frustration or anger. 9. Thoughts of self-harm or hopelessness. Remember, it's okay to seek help if these feelings persist. Reaching out to a mental health professional can provide the support and guidance you need.",
    ],
    r"what should i do if i’m worried about a friend or relative": [
        "It's commendable to be concerned about someone you care about. Here’s how you can offer support: 1. Open the conversation with care and empathy, expressing your worries without judgment. 2. Listen actively to what they share, providing a safe space for them to express their feelings. 3. If they seem distressed, gently encourage them to consider professional help and offer assistance in finding resources. 4. Help them with daily tasks if they’re struggling; this can alleviate some pressure. 5. Stay in touch regularly to check on their well-being, reinforcing that they’re not alone. 6. Encourage activities that promote self-care, which can help them cope better. Your support can be a vital part of their journey.",
    ],
    r"how do i deal with someone telling me what to do": [
        "It's common to feel frustrated when someone gives unsolicited advice. To handle this situation, consider: 1. Taking a deep breath and pausing before reacting. 2. Evaluating their intentions; often, they mean well. 3. Politely expressing your feelings by saying something like, 'I appreciate your concern, but I prefer to handle this my way.' 4. Setting boundaries by explaining your need for autonomy. 5. If it continues, you may need to distance yourself from that person's input when possible. Remember, it’s important to honor your own decisions and feelings.",
    ],
    r"can you prevent mental health problems": [
        "While it’s not always possible to prevent mental health issues, there are proactive steps you can take to enhance your well-being: 1. Prioritize self-care by maintaining a balanced diet, regular exercise, and sufficient sleep. 2. Foster strong social connections that provide support and encouragement. 3. Develop healthy coping strategies for managing stress, such as mindfulness or engaging in hobbies. 4. Limit alcohol and substance use, which can contribute to mental health challenges. 5. Stay informed about the signs of mental health issues so you can seek help early if needed. Taking care of your mental health is a lifelong journey.",
    ],
    r"what is substance abuse": [
        "Substance abuse refers to the harmful or hazardous use of psychoactive substances, including drugs and alcohol, often characterized by a compulsive pattern of use. This can lead to significant impairment or distress in daily functioning. According to medical sources, it involves using these substances for non-medical reasons or in ways not prescribed. Recognizing the signs of substance abuse is crucial for addressing potential issues and seeking appropriate help.",
    ],
    r"can someone visit an addiction mental health specialist for a relative": [
        "Yes, family members can certainly seek guidance from addiction specialists regarding their loved ones. Often, the family plays a critical role in recognizing addiction and motivating the individual to seek help. If the person is resistant to treatment, families can benefit from consultations to understand the situation better and explore supportive measures. This approach can empower families to assist their loved one effectively when they are ready to engage with professional support.",
    ],
    r".can i quit smoking on my own": [
        "Quitting smoking independently is definitely achievable for many people. However, it's important to recognize that some may benefit from additional support, such as counseling or medications designed to ease withdrawal symptoms and cravings. Setting a quit date, identifying triggers, and finding alternative coping mechanisms can significantly help. Remember, seeking support from friends, family, or support groups can also enhance your chances of success.",
    ],
    r"how do i know if i’m unwell": [
        "If you're questioning your well-being, it's essential to reflect on various aspects of your mental and emotional state. Common indicators that you might be struggling include: 1. Persistent feelings of sadness or anxiety. 2. Not enjoying activities you once loved. 3. Changes in eating or sleeping habits. 4. Difficulty focusing or making decisions. 5. Constant fatigue or low energy. 6. Feelings of hopelessness or guilt. 7. Withdrawing from friends and family. 8. Increased frustration or anger. 9. Thoughts of self-harm or hopelessness. Remember, it's okay to seek help if these feelings persist. Reaching out to a mental health professional can provide the support and guidance you need.",
    ],
    r"what should i do if i’m worried about a friend or relative": [
        "It's commendable to be concerned about someone you care about. Here’s how you can offer support: 1. Open the conversation with care and empathy, expressing your worries without judgment. 2. Listen actively to what they share, providing a safe space for them to express their feelings. 3. If they seem distressed, gently encourage them to consider professional help and offer assistance in finding resources. 4. Help them with daily tasks if they’re struggling; this can alleviate some pressure. 5. Stay in touch regularly to check on their well-being, reinforcing that they’re not alone. 6. Encourage activities that promote self-care, which can help them cope better. Your support can be a vital part of their journey.",
    ],
    r"how do i deal with someone telling me what to do": [
        "It's common to feel frustrated when someone gives unsolicited advice. To handle this situation, consider: 1. Taking a deep breath and pausing before reacting. 2. Evaluating their intentions; often, they mean well. 3. Politely expressing your feelings by saying something like, 'I appreciate your concern, but I prefer to handle this my way.' 4. Setting boundaries by explaining your need for autonomy. 5. If it continues, you may need to distance yourself from that person's input when possible. Remember, it’s important to honor your own decisions and feelings.",
    ],
    r"can you prevent mental health problems": [
        "While it’s not always possible to prevent mental health issues, there are proactive steps you can take to enhance your well-being: 1. Prioritize self-care by maintaining a balanced diet, regular exercise, and sufficient sleep. 2. Foster strong social connections that provide support and encouragement. 3. Develop healthy coping strategies for managing stress, such as mindfulness or engaging in hobbies. 4. Limit alcohol and substance use, which can contribute to mental health challenges. 5. Stay informed about the signs of mental health issues so you can seek help early if needed. Taking care of your mental health is a lifelong journey.",
    ],
    r"what is substance abuse": [
        "Substance abuse refers to the harmful or hazardous use of psychoactive substances, including drugs and alcohol, often characterized by a compulsive pattern of use. This can lead to significant impairment or distress in daily functioning. According to medical sources, it involves using these substances for non-medical reasons or in ways not prescribed. Recognizing the signs of substance abuse is crucial for addressing potential issues and seeking appropriate help.",
    ],
    r"can someone visit an addiction mental health specialist for a relative": [
        "Yes, family members can certainly seek guidance from addiction specialists regarding their loved ones. Often, the family plays a critical role in recognizing addiction and motivating the individual to seek help. If the person is resistant to treatment, families can benefit from consultations to understand the situation better and explore supportive measures. This approach can empower families to assist their loved one effectively when they are ready to engage with professional support.",
    ],
    r"can i quit smoking on my own": [
        "Quitting smoking independently is definitely achievable for many people. However, it's important to recognize that some may benefit from additional support, such as counseling or medications designed to ease withdrawal symptoms and cravings. Setting a quit date, identifying triggers, and finding alternative coping mechanisms can significantly help. Remember, seeking support from friends, family, or support groups can also enhance your chances of success.",
    ],
    r"what are the signs of stress": [
        "Stress can manifest in various ways, and recognizing the signs is essential for managing it effectively. Common indicators include: 1. Physical symptoms like headaches, stomachaches, or fatigue. 2. Emotional symptoms such as irritability, anxiety, or feeling overwhelmed. 3. Behavioral changes like increased use of alcohol or drugs, social withdrawal, or changes in eating habits. 4. Difficulty concentrating or making decisions. If you notice these signs in yourself or others, it may be time to explore stress management strategies or seek professional help.",
    ],
    r"how can i support someone dealing with anxiety": [
        "Supporting someone with anxiety can be incredibly valuable. Here are some ways to help: 1. Listen without judgment and validate their feelings. Let them know it’s okay to feel anxious. 2. Encourage them to seek professional help if they haven't already. 3. Help them identify triggers and develop coping strategies together. 4. Offer to accompany them to appointments or support groups if they feel comfortable. 5. Encourage relaxation techniques, such as deep breathing, meditation, or physical activity. Your understanding and support can make a significant difference in their journey.",
    ],
    r"what are coping strategies for depression": [
        "Coping with depression can be challenging, but there are several strategies that may help: 1. Establish a routine to create a sense of normalcy. 2. Engage in regular physical activity, which can boost mood. 3. Connect with friends or family members for support. 4. Practice mindfulness or meditation to stay grounded. 5. Seek professional help to explore therapy options. 6. Set small, achievable goals to create a sense of accomplishment. Remember, it’s important to be patient with yourself and seek help when needed.",
    ],
    r"how much alcohol is considered too much": [
        "When it comes to alcohol consumption, what's considered 'too much' can vary depending on several factors, including individual health, tolerance, and personal circumstances. Generally, moderate alcohol consumption is defined as up to one drink per day for women and up to two drinks per day for men. However, some individuals may still experience negative effects even within these limits. Seek advice from a healthcare professional if you have concerns.",
    ],
    r"can addictions be cured": [
        "Many people can recover from addiction, either spontaneously or with support. Others may experience relapses over time. Various treatment options, from harm reduction to rehabilitation, might be considered. Building a strong therapeutic relationship based on trust is essential for long-term recovery. Always reach out to professionals for help when needed.",
    ],
    r"is it normal for an older person living alone to be depressed": [
        "It's not normal for an older person living alone to be depressed, although it can often go untreated due to misconceptions about aging and depression. Many elderly people do not recognize the symptoms. Depression in older adults should be treated, and proper support is vital to improving their quality of life.",
    ],
    r"is psychotherapy a substitute for medication": [
        "Psychotherapy and medication serve different but complementary roles in mental health treatment. While medication helps manage certain symptoms, psychotherapy allows individuals to explore thoughts and emotions, develop coping strategies, and achieve personal growth. In some cases, a combination of both may be the best approach.",
    ],
    r"what should I do if I know someone who appears to have all the symptoms of a serious mental disorder": [
        "If someone shows signs of a serious mental disorder, express your concern, listen actively, and encourage them to seek professional help. Be supportive, but also respect their boundaries. If they're in immediate danger, involve professionals or a crisis helpline. Taking care of your own well-being is equally important while helping others.",
    ],
    r"what are some of the warning signs of mental illness": [
        "Some common warning signs of mental illness include: 1. Persistent sadness or mood changes. 2. Withdrawal from social activities. 3. Changes in sleep patterns. 4. Changes in appetite or weight. 5. Difficulty concentrating. 6. Unusual thoughts or beliefs. 7. Substance abuse. 8. Suicidal thoughts. If you or someone you know is experiencing any of these signs, seek help from a mental health professional.",
    ],
    r"how common are mental illnesses": [
        "Mental illnesses are quite common. According to the World Health Organization (WHO), about 1 in 4 people worldwide will experience a mental health issue at some point in their lives. These conditions can range from anxiety and depression to more severe disorders like schizophrenia.",
    ],
    r"can someone with a mental illness get better": [
        "Many people with mental illnesses can and do get better with the right support and treatment. Recovery may involve therapy, medication, lifestyle changes, and a strong support network. While setbacks are possible, with perseverance and the right resources, individuals can lead fulfilling lives after experiencing mental illness.",
    ],
    r"what psychological factors contribute to mental illness": [
        "Several psychological factors can contribute to mental illness, including: 1. Genetics and family history. 2. Trauma or adversity, such as abuse or neglect. 3. Biological factors like brain chemistry imbalances. 4. Unhealthy thought patterns, such as excessive self-criticism. 5. Personality traits like perfectionism. 6. Substance abuse. Mental illness is often the result of a combination of these factors.",
    ],
    r"what environmental factors contribute to mental illness": [
        "Environmental factors that contribute to mental illness include: 1. Stressful life events, such as trauma or loss. 2. Socioeconomic status and poverty. 3. High levels of job-related stress. 4. Exposure to violence. 5. Limited access to healthcare. 6. Cultural and societal stigmas surrounding mental health. It's important to note that mental health is influenced by a mix of genetic, psychological, and environmental factors.",
    ],
    r"can people get over mental illness without medication": [
        "Some individuals manage mental health issues without medication by engaging in regular therapy or counseling, such as cognitive-behavioral therapy (CBT).",
        "Lifestyle changes, like regular exercise and a balanced diet, can positively impact mental well-being and help individuals manage mental illness without medication.",
        "Mindfulness and meditation practices can be effective in reducing symptoms of mental illness without the need for medication.",
        "Support from family, friends, or peer support groups can help people manage mental health challenges without medication.",
        "Some individuals use self-help strategies like journaling, setting personal goals, or practicing gratitude to cope with mental illness.",
        "Creative outlets such as art, music, or writing can help individuals express emotions and manage mental health conditions without medication.",
        "Stress management techniques, including deep breathing exercises and progressive muscle relaxation, can aid in coping with mental illness without medication.",
        "Spending time in nature and engaging in outdoor activities has been shown to improve mental health and may help some people avoid medication.",
        "Building a structured routine can help people manage their symptoms and improve mental well-being without relying on medication.",
        "For some, focusing on maintaining strong relationships and social connections serves as a key factor in managing mental illness without medication.",
    ],
    r"does exercising help control mental illness by itself": [
        "Exercise alone may not fully control mental illness, but it can be a valuable part of a broader mental health management plan."
    ],
    r"can exercise alone cure mental health issues": [
        "Exercise, while beneficial, is typically not enough on its own to cure mental health issues; therapy or medication might be necessary."
    ],
    r"is physical activity enough to treat mental illness": [
        "Physical activity helps improve mood and reduce stress, but mental illness treatment usually requires more than just exercise."
    ],
    r"can workouts alone manage mental health disorders": [
        "Workouts alone may not be sufficient to manage mental health disorders, but they are an excellent complement to therapy and medication."
    ],
    r"can you stabilize mental health with exercise only": [
        "Exercise can improve mental well-being, but stabilizing mental health often requires additional interventions like counseling or medication."
    ],
    r"does fitness cure depression": [
        "Fitness can alleviate symptoms of depression and anxiety, but it is usually more effective when combined with therapy or medication."
    ],
    r"is working out enough to manage mental illness": [
        "Working out contributes to mental health, but it's often not enough on its own to manage complex mental illnesses."
    ],
    r"does regular exercise prevent mental health disorders": [
        "Regular exercise can help prevent certain mental health issues, but it's not a guaranteed prevention method for all disorders."
    ],
    r"does exercise help control mental health without meds": [
        "Exercise can help control symptoms of mental health conditions, but it often works best when paired with other treatments."
    ],
    r"can exercise alone treat mental illness": [
        "Exercise alone may not fully treat mental illness, but it can significantly contribute to overall mental well-being."
    ],
    r"Where Can I Learn About Types Of Mental Health Treatment": [
        "You can explore reliable sources such as mental health websites, professional therapists, books, support groups, and online communities to learn about types of mental health treatment."
    ],
    r"Where Can I Go To Find A Support Group": [
        "You can find a support group through online resources, local mental health organizations, hospitals, your therapist, social media, and support apps."
    ],
    r"Is mental health genetic": [
        "Yes, mental health can have a genetic component, but it is influenced by both genetic and environmental factors."
    ],
    r"How does mental health affect physical health": [
        "Mental health impacts physical health through stress, sleep disturbances, appetite, heart health, chronic pain, and inflammation."
    ],
    r"Can mental health cause seizures": [
        "Yes, stress and emotional factors can sometimes trigger seizures, such as psychogenic nonepileptic seizures, which are linked to psychological distress."
    ],
    r"How can mental health issues lead to addiction.*": [
        "Mental health issues can lead to addiction when individuals use substances to self-medicate, creating a harmful cycle of dependency."
    ],
    r"Who should I talk to about mental health": [
        "You should talk to a mental health professional like a psychologist, psychiatrist, or therapist, or someone you trust, like a friend or family member."
    ],
    r"What is the difference between a psychiatrist, a psychologist, and a therapist": [
        "Psychiatrists are medical doctors who can prescribe medication, psychologists focus on therapy, and therapists may have various counseling backgrounds."
    ],
    r"What’s the difference between psychotherapy and counseling": [
        "Psychotherapy often addresses diagnosable mental health conditions, while counseling focuses on overall wellness and problem-solving strategies."
    ],
    r"What types of mental illness and mental health problems can be treated by a psychiatrist": [
        "Psychiatrists treat various disorders, including depression, anxiety, schizophrenia, PTSD, OCD, and substance use disorders, using medication and therapy."
    ],
    r".*difference between anxiety and stress.*": [
        "While the physical sensations of anxiety and stress can be similar, their causes are usually different. Stress is usually caused by external pressures we’re having difficulty coping with. When we’re stressed, we usually know what we’re stressed about, and the symptoms of stress generally resolve themselves once the stressful situation ends. Anxiety, on the other hand, is usually caused by worries or fears about potential threats or troubles."
    ],
    r".*difference between sadness and depression.*": [
        "Sadness is a normal reaction to some of life’s challenges. If your feelings of sadness resolve themselves on their own over time and don’t impact your life in a big way, you’re probably not dealing with depression."
    ],
    r".*how do you know if you have an addiction.*": [
        "Common signs of addiction include loss of control, withdrawal symptoms, neglecting responsibilities, tolerance, cravings, and isolation."
    ],
    r".*are mental health problems common.*": [
        "Yes, mental health problems are indeed common and affect millions of people worldwide."
    ],
    r".*how can I get help paying for my medication.*": [
        "Some pharmaceutical companies offer prescription assistance programs, and you can also look for prescription discount cards or coupons."
    ],
    r".*if I feel better after taking medication, can I stop.*": [
        "It's important to consult your healthcare provider before making any changes to your medication regimen, as stopping suddenly can lead to withdrawal symptoms."
    ],
    r".*what should I know before starting a new medication.*": [
        "Always consult with a qualified healthcare professional and familiarize yourself with potential side effects."
    ],
    r".*what happens in a therapy session.*": [
        "Therapy is a supportive process where you'll discuss your thoughts and feelings with your therapist."
    ],
    r".*how long can I expect to be in therapy.*": [
        "The duration of therapy varies; some may find relief in a few weeks, while others may benefit from longer treatment."
    ],
    r".*are neurofeedback and biofeedback the same thing.*": [
        "Neurofeedback is a type of biofeedback specifically targeting brainwave patterns."
    ],
    r".*medication can cause sexual side effects.*": [
        "Yes, certain medications can cause sexual side effects, such as changes in libido or difficulty achieving arousal. These effects may be temporary or, in some cases, persist even after stopping the medication. Always consult your healthcare provider before making any changes to your medication."
    ],
    r".*will I become addicted to the medication.*": [
        "Addiction typically involves craving a drug despite negative consequences. Most psychiatric medications do not pose a significant risk of addiction. It's important to discuss any concerns with your doctor or pharmacist."
    ],
    r".*why do psychiatric medications cost so much.*": [
        "The cost of psychiatric medications can be high due to research and development expenses, ongoing monitoring by healthcare professionals, and the influence of patents. Generic alternatives usually become available after patent expiration, potentially lowering costs."
    ],
    r".*long-term effects of taking medication for mental illness.*": [
        "Most psychiatric medications are safe when taken as prescribed. However, some may impact organs like the liver or kidneys, especially with long-term use. Regular check-ups are important to monitor any potential side effects."
    ],
    r".*friend has mental illness but stops taking medication.*": [
        "Encourage open communication, educate yourself about their condition, and offer non-judgmental support. Help them identify triggers and encourage professional help when needed."
    ],
    r".*antidepressant may increase suicidal thoughts.*": [
        "It's important to discuss any concerns about suicidal thoughts with your healthcare provider. Open communication is essential during your medication journey."
    ],
    r".*negative effects associated with stopping antidepressants.*": [
        "Yes, abruptly stopping antidepressants can lead to withdrawal symptoms. It's crucial to consult your doctor before discontinuing any medication."
    ],
    r".*take medication for the rest of my life.*": [
        "Long-term treatment may be necessary for some individuals, similar to managing other chronic conditions. Discuss your treatment options and concerns with your doctor."
    ],
    r".*facts about Mental Health.*": [
        "1. 1 in 5 young people suffers from mental illness. 2. Suicide is a leading cause of death among young people. 3. Over 2/3 of young people do not seek help for mental health issues."
    ],
    r".*insomnia disorder.*": [
        "Insomnia disorder is characterized by dissatisfaction with sleep quality or quantity, with symptoms occurring at least three times a week for three months, causing distress or functional impairment."
    ],
    r".*major depressive disorder (MDD).*": [
        "Major depressive disorder (MDD) is diagnosed when a person has at least five symptoms, including persistently low mood, decreased interest in activities, and feelings of worthlessness."
    ],
    r".*help mental health while living with prostate cancer.*": [
        "Talk to someone about your feelings, educate yourself about your condition, join support groups, practice mindfulness, engage in physical activity, and pursue hobbies to help maintain your mental health."
    ],
    r".*racial trauma.*": [
        "Racial trauma refers to the psychological harm experienced due to racism or discrimination. It can lead to symptoms like anxiety and depression. Seeking support from knowledgeable mental health professionals can aid in healing."
    ],
    r"being stressed gives me discomfort": ["You should try meditation"],
    r"being stressed gives me the feeling of uneasiness": [
        "You should try meditation and taking deep breaths if you ever feel this way again"
    ],
    # breakup
    r"I can't stop thinking about her. It's consuming my every waking moment.": [
        "It's common to feel preoccupied after a breakup. Can you tell me more about what thoughts are recurring?"
    ],
    r"I can't stop thinking about him. It's consuming my every waking moment.": [
        "It's common to feel preoccupied after a breakup. Can you tell me more about what thoughts are recurring?"
    ],
    r"I'm having trouble focusing at work. Everything seems pointless now.": [
        "A loss can certainly impact our daily functioning. How has your performance at work been affected?"
    ],
    r"I keep wondering if I'll ever feel happy again. Is this normal?": [
        "Questioning future happiness is a common reaction. What does happiness look like to you right now?"
    ],
    r"I'm angry all the time. I snap at my friends and family for no reason.": [
        "Anger is a natural part of grief. How do you typically handle anger in other situations?"
    ],
    r"I've lost my appetite completely. I can't remember the last time I ate a full meal.": [
        "Changes in appetite are common during emotional distress. How else has the breakup affected your daily routine?"
    ],
    r"I keep having dreams about them. It's like my subconscious won't let me move on.": [
        "Dreams can be our mind's way of processing emotions. How do these dreams make you feel when you wake up?"
    ],
    r"I'm tempted to call them every day. I've almost done it several times.": [
        "The urge to reconnect is strong after a breakup. What's stopping you from making that call?"
    ],
    r"I feel like I've lost part of my identity. We were together for so long.": [
        "Long-term relationships often become part of our self-image. What aspects of yourself do you feel you've lost?"
    ],
    r"I'm scared of being alone. I don't know how to do this by myself.": [
        "The prospect of being single can be daunting. What specifically about being alone frightens you?"
    ],
    r"I keep replaying all our good memories. It makes it hard to accept it's over.": [
        "Nostalgia can be bittersweet after a breakup. How do these memories affect your current emotions?"
    ],
    r"I'm embarrassed to tell people we've broken up. It feels like admitting failure.": [
        "It's common to feel that way. Why do you think you see the breakup as a failure?"
    ],
    r"I'm having trouble sleeping. My mind races as soon as I lie down.": [
        "Sleep disturbances are common during emotional upheaval. What thoughts come to mind when you're trying to sleep?"
    ],
    r"I feel like I'm on an emotional rollercoaster. One minute I'm okay, the next I'm a mess.": [
        "Emotional fluctuations are normal after a significant loss. Can you describe a recent situation where your emotions shifted quickly?"
    ],
    r"I keep second-guessing every decision I make now. I've lost all confidence.": [
        "A breakup can shake our self-assurance. In what areas of your life are you feeling the most uncertain?"
    ],
    r"I'm worried I'll never trust anyone again. How can I open up after this?": [
        "Trust issues are common after a painful breakup. What aspects of trust feel most challenging to you right now?"
    ],
    r"I feel like I'm grieving, but they're not dead. Is this normal?": [
        "The end of a relationship can indeed feel like a death. How would you describe your grieving process?"
    ],
    r"I'm struggling to find meaning in anything. Everything feels pointless.": [
        "A loss can certainly impact our sense of purpose. What gave your life meaning before the breakup?"
    ],
    r"I keep wondering what they're doing now. Are they as upset as I am?": [
        "It's natural to wonder about your ex's emotional state. How does thinking about their current state affect you?"
    ],
    r"I'm afraid I'll never find someone else. What if this was my only chance?": [
        "Fear of future loneliness is common. What makes you think this was your only chance at love?"
    ],
    r"I feel like I'm falling behind in life. All my friends are in relationships.": [
        "It's easy to compare ourselves to others, especially after a breakup. How does this comparison affect your self-image?"
    ],
    r"I'm having trouble remembering the bad times. Was it really as good as I remember?": [
        "Our memories can be selective after a breakup. Why do you think you're focusing on the positive memories?"
    ],
    r"I keep blaming myself for everything that went wrong. Is it all my fault?": [
        "Self-blame is a common reaction. What specific things are you blaming yourself for?"
    ],
    r"I'm scared to start dating again. The thought of putting myself out there terrifies me.": [
        "Fear of reentering the dating world is normal. What aspects of dating feel most daunting to you?"
    ],
    r"I feel like I've lost my best friend. I don't know who to talk to anymore.": [
        "The loss of a partner can also mean the loss of a confidant. How has this affected your support system?"
    ],
    r"I'm worried I'll always feel this way. Will the pain ever go away?": [
        "It's common to feel that the pain is permanent. What makes you think it might not improve?"
    ],
    r"I keep wondering if I should have fought harder to make it work.": [
        "Questioning our efforts is natural after a breakup. What makes you think you didn't fight hard enough?"
    ],
    r"I'm having trouble finding joy in things I used to love. Everything feels tainted now.": [
        "Loss of interest in previously enjoyable activities is common. Can you tell me more about what you used to enjoy?"
    ],
    r"I feel like I'm going backwards in life. Like I've lost all the progress I made.": [
        "A breakup can certainly feel like a setback. In what ways do you feel you've lost progress?"
    ],
    r"I feel like I'm going backwards in life.": [
        "A breakup can certainly feel like a setback. In what ways do you feel you've lost progress?"
    ],
    r"I'm worried about running into him. I don't know how I'll react.": [
        "Anxiety about potential encounters is normal. What specifically concerns you about seeing them?"
    ],
    r"I'm worried about running into her. I don't know how I'll react.": [
        "Anxiety about potential encounters is normal. What specifically concerns you about seeing them?"
    ],
    r"I keep wondering if there's something fundamentally wrong with me. Why can't I make relationships work?": [
        "It's common to question ourselves after a breakup. What makes you think there might be something wrong with you?"
    ],
    r"Not really. I've been too focused on the breakup to try anything new": [
        "It can be difficult to shift focus, but trying something new could help break the cycle of repetitive thoughts."
    ],
    r"I've thought about it, but I'm not sure what to do": [
        "What's something you've always wanted to try but never had the time for?"
    ],
    r"I've always wanted to learn to play the guitar, but it felt like a big commitment": [
        "That sounds like a great way to channel your energy. It doesn't have to be a big commitment—just a small start."
    ],
    r"Maybe I'll give it a try. It could be a good distraction": [
        "It's more than just a distraction. It's also a way to invest in yourself and create new positive experiences."
    ],
    r"You're right. I think I could benefit from that": [
        "Have you experienced any changes in your routine since the breakup?"
    ],
    r"My routine has been all over the place. I'm not sleeping well, and I've been skipping meals": [
        "Breakups can disrupt our daily habits. It's important to take care of your basic needs, even when it's hard."
    ],
    r"I know, but it's tough to find the motivation": [
        "Start with small steps. Could you try setting a goal to eat at least one healthy meal and get some rest tonight?"
    ],
    r"I'll try, but it feels like everything is out of balance": [
        "It may feel that way now, but slowly re-establishing routine can help restore a sense of stability."
    ],
    r"I could see that. I'll try to get back into some sort of rhythm": [
        "Even a small change can have a big impact on how you feel. Take it one day at a time."
    ],
    r"I'll do my best. I guess it's better than staying in this slump": [
        "Have you given any thought to what you want for yourself in the future, outside of this relationship?"
    ],
    r"I'll do my best. I guess it's better than staying in this slump": [
        "Have you given any thought to what you want for yourself in the future, outside of this relationship?"
    ],
    r"I’ve been so focused on what I’ve lost that I haven’t thought much about the future": [
        "It’s understandable to feel that way, but thinking about your future goals can help create a sense of hope."
    ],
    r"I used to have a lot of goals, but they all feel out of reach now": [
        "Those goals may feel distant, but they’re still within your reach. What’s one thing you’d like to focus on for your personal growth?"
    ],
    r"I guess I’d like to work on my confidence. I relied on my ex for that, and now I feel insecure": [
        "Building confidence within yourself is a powerful goal. What’s one way you could start working toward that?"
    ],
    r"Maybe I could take a course or join a group where I can meet new people and step out of my comfort zone": [
        "That sounds like a great step toward independence and self-assurance."
    ],
    r"I’ll look into it. It’s scary, but I think it could help": [
        "Have you been replaying moments from the relationship in your mind?"
    ],
    r"Constantly. I keep wondering if there was something I could have done differently": [
        "It’s natural to reflect on what went wrong, but it’s important not to blame yourself entirely. Relationships are complex."
    ],
    r"I just can’t help but think that maybe if I had tried harder, things would have been different": [
        "While it’s valuable to learn from the past, it’s also crucial to recognize that both people contribute to the relationship’s dynamics."
    ],
    r"I know, but it still feels like I failed": [
        "Feeling like you failed can be part of the healing process, but it’s important to remember that failure is not the end—it’s an opportunity to grow."
    ],
    r"I guess I need to be kinder to myself during this process": [
        "Absolutely. Self-compassion is key to moving forward."
    ],
    r"It’s hard, but I’ll try to be more forgiving of myself": [
        "Have you noticed any changes in how you view yourself since the breakup?"
    ],
    r"I’ve felt a lot less confident. The breakup made me question my worth": [
        "Breakups can shake our self-esteem, but it’s important to remember that your worth isn’t determined by someone else’s decision."
    ],
    r"It’s hard not to see it that way when they chose to leave": [
        "I understand. It may feel like rejection defines your value, but it doesn’t. What are some qualities you appreciate about yourself?"
    ],
    r"I used to think I was kind and thoughtful, but now I just feel like I wasn’t enough": [
        "Those are important qualities, and they’re still true about you. The breakup doesn’t take that away."
    ],
    r"I guess I need to work on remembering that": [
        "It’s a process, but reinforcing your positive qualities can help rebuild your sense of self-worth."
    ],
    r"I’ll try to focus on that instead of what I feel I’ve lost": [
        "Do you feel any resentment toward your ex?"
    ],
    r"Definitely. I’m angry that they moved on so quickly while I’m still struggling": [
        "It’s natural to feel resentment, especially when it feels like you’re carrying more of the emotional weight."
    ],
    r"Yeah, it feels like I’m stuck in pain while they’re fine": [
        "Everyone processes breakups differently. Their journey doesn’t invalidate your feelings, but it’s important to focus on your own healing."
    ],
    r"I know I shouldn’t compare, but it’s hard not to": [
        "It’s challenging, but comparison often prolongs pain. Can you shift your focus to how you can heal at your own pace?"
    ],
    r"I’ll try. I guess I just need to remind myself that healing looks different for everyone": [
        "Exactly. Your healing journey is unique to you, and it’s okay to take the time you need."
    ],
    r"That’s reassuring to hear. I’ll try to be more patient with myself": [
        "It’s understandable to feel that way, but thinking about your future goals can help create a sense of hope."
    ],
    r"I used to have a lot of goals, but they all feel out of reach now": [
        "Those goals may feel distant, but they’re still within your reach. What’s one thing you’d like to focus on for your personal growth?"
    ],
    r"I guess I’d like to work on my confidence. I relied on my ex for that, and now I feel insecure": [
        "Building confidence within yourself is a powerful goal. What’s one way you could start working toward that?"
    ],
    r"Maybe I could take a course or join a group where I can meet new people and step out of my comfort zone": [
        "That sounds like a great step toward independence and self-assurance."
    ],
    r"I’ll look into it. It’s scary, but I think it could help": [
        "Have you been replaying moments from the relationship in your mind?"
    ],
    r"Constantly. I keep wondering if there was something I could have done differently": [
        "It’s natural to reflect on what went wrong, but it’s important not to blame yourself entirely. Relationships are complex."
    ],
    r"I just can’t help but think that maybe if I had tried harder, things would have been different": [
        "While it’s valuable to learn from the past, it’s also crucial to recognize that both people contribute to the relationship’s dynamics."
    ],
    r"I know, but it still feels like I failed": [
        "Feeling like you failed can be part of the healing process, but it’s important to remember that failure is not the end—it’s an opportunity to grow."
    ],
    r"I guess I need to be kinder to myself during this process": [
        "Absolutely. Self-compassion is key to moving forward."
    ],
    r"It’s hard, but I’ll try to be more forgiving of myself": [
        "Have you noticed any changes in how you view yourself since the breakup?"
    ],
    r"I’ve felt a lot less confident. The breakup made me question my worth": [
        "Breakups can shake our self-esteem, but it’s important to remember that your worth isn’t determined by someone else’s decision."
    ],
    r"It’s hard not to see it that way when they chose to leave": [
        "I understand. It may feel like rejection defines your value, but it doesn’t. What are some qualities you appreciate about yourself?"
    ],
    r"I used to think I was kind and thoughtful, but now I just feel like I wasn’t enough": [
        "Those are important qualities, and they’re still true about you. The breakup doesn’t take that away."
    ],
    r"I guess I need to work on remembering that": [
        "It’s a process, but reinforcing your positive qualities can help rebuild your sense of self-worth."
    ],
    r"I’ll try to focus on that instead of what I feel I’ve lost": [
        "Do you feel any resentment toward your ex?"
    ],
    r"Definitely. I’m angry that they moved on so quickly while I’m still struggling": [
        "It’s natural to feel resentment, especially when it feels like you’re carrying more of the emotional weight."
    ],
    r"Yeah, it feels like I’m stuck in pain while they’re fine": [
        "Everyone processes breakups differently. Their journey doesn’t invalidate your feelings, but it’s important to focus on your own healing."
    ],
    r"I know I shouldn’t compare, but it’s hard not to": [
        "It’s challenging, but comparison often prolongs pain. Can you shift your focus to how you can heal at your own pace?"
    ],
    r"I’ll try. I guess I just need to remind myself that healing looks different for everyone": [
        "Exactly. Your healing journey is unique to you, and it’s okay to take the time you need."
    ],
    r"That’s reassuring to hear. I’ll try to be more patient with myself": [
        "Therapist: Have you been feeling any guilt about the breakup?"
    ],
    r"A lot. I keep thinking that I could have done more to save the relationship": [
        "Guilt is a common emotion after a breakup, but relationships are a two-way street. It’s not all on you."
    ],
    r"I know, but it feels like I should have seen it coming and done something to fix it": [
        "It’s natural to reflect on what you could have done differently, but it’s important to acknowledge that you can’t control everything."
    ],
    r"I guess I’m just struggling to accept that I couldn’t fix it": [
        "Acceptance is hard, but it’s a necessary step toward healing. Sometimes, even our best efforts can’t change the outcome."
    ],
    r"I know you’re right. It just feels like such a heavy weight to carry": [
        "It is a heavy weight, but by letting go of some of that guilt, you’ll feel lighter over time."
    ],
    r"I hope so. I’m ready to let go of this feeling eventually": [
        "How are you handling social situations since the breakup?"
    ],
    r"I’ve been avoiding them. I don’t feel like being around people right now": [
        "That’s a common response, but social connection can actually help in the healing process, even if it’s just with a close friend."
    ],
    r"I’ve been pushing everyone away because I don’t want to talk about the breakup": [
        "It’s understandable to want space, but is there someone you trust who could support you without pressuring you to talk about it?"
    ],
    r"Maybe. I have a friend who’s been reaching out, but I haven’t responded": [
        "It might help to reconnect, even if you don’t talk about the breakup. Just being around someone who cares could be comforting."
    ],
    r"You’re right. I’ll reach out to them and see how it goes": [
        "That’s a great step."
    ],
    r"Why do I feel like I’ll never be happy again after this breakup?": [
        "It’s common to feel that way after a breakup because the loss can feel overwhelming. Right now, you’re grieving, and in that space, happiness may seem distant. But these feelings will evolve over time as you begin to heal. It’s important to remember that emotions are temporary and that with patience and self-compassion, you will find happiness again."
    ],
    r"I can’t stop checking my ex’s social media. Is that normal?": [
        "Yes, it’s a very normal reaction. After a breakup, many people find themselves seeking information about their ex as a way to feel connected. However, this can make it harder to move on. Consider setting boundaries with yourself when it comes to social media. Taking breaks from checking your ex’s accounts can help you focus on your healing."
    ],
    r"How do I know if I’m ready to date again?": [
        "You might be ready to date again when you feel like you’ve processed the breakup, when thoughts of your ex no longer dominate your mind, and when you’re comfortable being on your own. It’s important to ensure you’re not dating just to fill a void but because you genuinely feel open to new experiences. Take your time and trust your intuition."
    ],
    r"Is it a bad idea to reach out to my ex for closure?": [
        "Seeking closure is a natural desire, but it’s important to reflect on what you hope to gain from the conversation. Sometimes, reaching out can reopen old wounds rather than bring the peace you’re looking for. If you feel it will help you heal, it might be worth doing, but make sure you’re emotionally prepared for whatever response you may get—or even if you don’t get one at all."
    ],
    r"I keep blaming myself for the breakup. How do I stop?": [
        "It’s common to replay events in your mind and feel like you’re at fault, but it’s important to remember that relationships are a two-way street. Breakups rarely happen because of just one person. Try to focus on what you learned from the relationship rather than placing blame. Acknowledge that you did the best you could with the information and emotions you had at the time. Self-compassion is key in this process."
    ],
    r"I feel like my ex has moved on so easily, and I’m still stuck. Why is that?": [
        "Everyone processes breakups differently. It may seem like your ex has moved on quickly, but you can’t always know what they’re truly feeling. Healing isn’t a race, and it’s okay if you’re taking more time to process. Focus on your own journey, and give yourself the space you need to heal."
    ],
    r"I keep having dreams about my ex, and it’s messing with my head. What does that mean?": [
        "Dreams are often our mind’s way of processing emotions, especially when they’re unresolved or intense. It’s normal to dream about your ex after a breakup since they were a significant part of your life. Over time, as you heal and come to terms with the breakup, those dreams will likely decrease."
    ],
    r"Should I try to stay friends with my ex, or is it better to cut contact?": [
        "Staying friends with an ex can work for some, but it depends on whether both parties have truly moved on and can handle that dynamic. If the friendship is causing more pain or confusion, it might be best to take some time apart to heal. It’s important to prioritize your emotional well-being in this decision."
    ],
    r"How do I stop constantly thinking about what could have been?": [
        "It’s natural to reflect on what could have been after a breakup, but dwelling on those thoughts can prevent you from moving forward. Try focusing on the reality of the situation rather than the ‘what-ifs.’ You can’t change the past, but you can shape your future. Redirect your energy into things that make you feel empowered."
    ],
    r"I’m scared of being alone. How do I cope with this feeling?": [
        "Fear of being alone is a common feeling after a breakup, especially if the relationship was a big part of your identity. It’s important to reconnect with yourself and learn to enjoy your own company. Start by finding small activities that bring you joy or peace. Over time, being alone can feel less like loneliness and more like self-care."
    ],
    r"I feel so much anger toward my ex. How can I deal with this rage?": [
        "Anger is a valid emotion after a breakup, especially if you feel hurt or betrayed. It’s important to find healthy ways to express and process that anger—whether it’s through journaling, talking to someone you trust, or physical activity. Over time, you may find that the anger lessens as you work through your emotions."
    ],
    r"I can’t bring myself to delete our old photos. Is that okay?": [
        "It’s understandable that you may not be ready to delete photos, as they hold memories. Give yourself permission to keep them for now if it feels too painful to let them go. When you feel more emotionally ready, you can revisit the idea of deleting them or saving them in a way that doesn’t trigger sadness."
    ],
    r"My ex already has a new partner, and it’s tearing me apart. How do I deal with this?": [
        "Seeing your ex with someone new can be incredibly painful, especially if you’re still healing. It’s important to remind yourself that their new relationship doesn’t diminish your worth or invalidate the time you spent together. Try to limit your exposure to information about your ex’s new life and focus on your own healing process."
    ],
    r"I feel like I’ll never find love again. What if I’m never able to move on?": [
        " It’s natural to feel that way after a breakup, but these feelings don’t last forever. Healing takes time, and with patience, you’ll find that your perspective shifts. Love can come again when you’re ready, but for now, it’s okay to focus on loving yourself and taking care of your emotional needs."
    ],
    r"Should I block my ex on social media, or would that be immature?": [
        "Blocking your ex isn’t immature if it’s what you need to protect your emotional well-being. Sometimes creating distance—especially online—can help you heal without constant reminders of the past. It’s a personal decision, and it’s okay to prioritize what feels healthiest for you."
    ],
    r"I don’t know how to stop feeling lonely after my breakup. What can I do?": [
        "Loneliness after a breakup is very common, especially when you’ve been used to having someone close. It can help to reconnect with friends or family and engage in activities you enjoy. Building a support network and staying socially active, even in small ways, can ease feelings of loneliness."
    ],
    r"I feel like I’ll never trust anyone again after this. How do I rebuild trust?": [
        "Trust takes time to rebuild, especially after a painful experience like a breakup. Start by focusing on healing and regaining trust in yourself. As you process your emotions, you’ll gradually feel more open to trusting others again. It’s okay to take things slowly and set boundaries when you’re ready to engage in future relationships."
    ],
    r"I’ve been drinking more to cope with the pain. Is that a problem?": [
        "Turning to alcohol or other substances to cope can temporarily numb the pain, but it’s not a healthy long-term solution. It can actually delay healing. If you’re noticing this pattern, it’s important to find healthier ways to manage your emotions—like talking to someone, exercising, or engaging in activities that help you process your feelings."
    ],
    r"I keep hoping my ex will come back. Should I hold onto that hope?": [
        "It’s natural to want reconciliation, but it’s important to focus on what’s best for your long-term well-being. Holding onto hope can sometimes prevent you from moving forward. Consider focusing on your healing, and if reconciliation is meant to happen, it will come in time. Meanwhile, allowing yourself to heal can help you feel stronger, whether or not your ex returns."
    ],
    r"I’m afraid of getting hurt again in the future. How do I overcome that fear?": [
        "After experiencing heartbreak, it’s normal to fear getting hurt again. It’s important to acknowledge that fear but not let it stop you from moving forward when you’re ready. Take the time to heal and reflect on what you’ve learned from the past. When you feel ready to open up again, it can help to take things slowly and communicate openly with future partners."
    ],
    r"I feel guilty for ending the relationship. How do I deal with that?": [
        "It’s normal to feel guilty, especially if you cared deeply about the other person. Ending a relationship is difficult, but it’s important to remind yourself that you made the decision for a reason. Take time to reflect on why it was the best choice for both of you, and focus on forgiving yourself as part of your healing."
    ],
    r"I keep thinking about the good times we had, and it makes me want to reach out. Should I?": [
        "It’s natural to reminisce about the good moments, but it’s important to remember why the relationship ended. Reaching out might reignite old feelings and delay your healing. Try focusing on the present and how you can create positive experiences for yourself now. Giving yourself space can help you gain clarity."
    ],
    r"I’m afraid that I’ll never feel as connected to someone again. What if I never meet anyone like my ex?": [
        "It’s common to feel like no one will compare to your ex, especially right after a breakup. However, connections form differently with each person, and while it may take time, you will likely find new relationships that bring their own unique value. Healing will help you feel open to new connections when the time is right."
    ],
    r"I’ve started dating again, but I can’t help comparing everyone to my ex. How do I stop?": [
        "Comparing new people to your ex is a common part of healing, especially if your ex is still on your mind. It’s important to give yourself time to fully heal before jumping into a new relationship. Focus on getting to know each person for who they are, without the lens of your past relationship."
    ],
    # Depression
    r"I feel sad all the time, but I don’t even know why. Is this normal?": [
        "It’s common to feel overwhelmed by sadness, especially if it feels like it’s coming from nowhere. Depression can sometimes occur without a clear cause, but that doesn’t mean your feelings aren’t valid. It’s important to explore what might be contributing to those emotions and take steps to care for your mental well-being."
    ],
    r"I can’t get out of bed most days. I just don’t have the energy. What’s wrong with me?": [
        "Lack of energy and motivation are key signs of depression. It can make even small tasks feel overwhelming. It’s important to be gentle with yourself. Taking small steps each day, even if it’s just getting out of bed or doing one task, can help you gradually regain some of that energy."
    ],
    r"I feel like I’m not good enough, no matter what I do. How can I stop feeling this way?": [
        "Depression can often distort our perception of ourselves, making us feel inadequate. It’s important to challenge these negative thoughts by recognizing your strengths and accomplishments. Practice self-compassion and remind yourself that you are worthy, regardless of what depression tells you."
    ],
    r"I feel like nothing matters anymore. I don’t see the point in trying.": [
        "Depression can make everything feel meaningless, but it’s important to remember that this feeling is part of the condition, not reality. Finding small moments of purpose or joy, even in the little things, can help. Reconnecting with things you used to enjoy, even if they don’t feel exciting right now, can also be a step toward rediscovering meaning."
    ],
    r"I’ve been isolating myself from my friends and family because I just don’t want to see anyone.": [
        "Depression often makes us withdraw from the people we care about, even though staying connected can be helpful for our mental health. It’s okay to take time for yourself, but try to reach out to someone you trust, even if it’s just for a small chat. Social connection can sometimes break through the isolation."
    ],
    r"I can’t seem to focus on anything. My mind feels foggy all the time.": [
        "Concentration difficulties and 'brain fog' are common symptoms of depression. It can help to break tasks into smaller, more manageable steps. Focus on one thing at a time, and give yourself permission to take breaks. Over time, as you work on managing your depression, your ability to concentrate should improve."
    ],
    r"I feel like I’m a burden to everyone around me. Maybe they’d be better off without me.": [
        "Feeling like a burden is a common thought in depression, but it’s important to remember that the people who care about you don’t see you that way. Depression distorts our thinking, making us feel less valuable. It’s crucial to reach out for support during these moments, whether it’s to a friend, family member, or therapist."
    ],
    r"Nothing seems to make me happy anymore. I don’t enjoy the things I used to love.": [
        "Loss of interest in activities, known as anhedonia, is a hallmark symptom of depression. Even though you may not feel joy right now, try to continue engaging in those activities. Sometimes, going through the motions can eventually help you reconnect with what once brought you happiness."
    ],
    r"I feel like I’m stuck in a black hole. No matter what I do, I can’t get out of it.": [
        "Depression can feel like a deep, inescapable pit, but it’s important to know that you’re not alone in this. Recovery from depression often involves small, gradual steps. Whether it’s through therapy, lifestyle changes, or medication, there are ways to climb out of that dark place. It might take time, but you don’t have to stay there."
    ],
    r"I’ve been crying for no reason, and I feel so drained afterward. What’s happening to me?": [
        "Crying without a clear reason can be a sign of emotional overwhelm, which is common in depression. Your body and mind are processing emotions, even if you can’t identify the cause. It’s important to give yourself time to rest and recover after these moments and consider reaching out for support to talk through your feelings."
    ],
    r"I feel like I’m just going through the motions. Life feels empty and meaningless.": [
        "Depression can make everyday life feel hollow, like you’re just existing rather than living. One way to combat this is by finding small moments of purpose or setting tiny goals that give you something to work toward. Reintroducing structure into your day can also help create a sense of meaning."
    ],
    r"I keep feeling like I’m failing at everything. How do I deal with that?": [
        "Depression often warps our perception, making us feel like failures even when we’re not. It can help to look at the evidence—acknowledge your achievements, no matter how small they seem. Challenge the negative thoughts and remind yourself that progress doesn’t have to be perfect."
    ],
    r"I’m always tired, no matter how much I sleep. Is this related to my depression?": [
        "Yes, depression can cause persistent fatigue, even if you’re getting enough sleep. It’s part of how depression affects both your body and mind. Focusing on a balanced routine that includes healthy sleep, nutrition, and some form of physical activity can help combat this fatigue, though it may take time."
    ],
    r"I don’t think anyone understands what I’m going through. I feel so alone.": [
        "Depression can make us feel isolated, even when others care about us. While it might seem like no one understands, there are people who can relate to what you’re feeling. Opening up about your experience, whether to a trusted friend, family member, or therapist, can help bridge that gap and reduce the feeling of loneliness."
    ],
    r"I feel like I’ll never get better. What if this lasts forever?": [
        "It’s understandable to feel hopeless during depression, but recovery is possible. It may not be a straight path, but with time, support, and the right treatment, you can feel better. Each small step you take, whether through therapy, self-care, or other methods, brings you closer to healing. You don’t have to go through this alone."
    ],
    r"I have depression": [
        "I wont be able to find out much if you dont clarify. Depression can be caused by various things"
    ],
    # BoardGame
    r"Why do I feel like this all the time?": [
        "It could be due to unresolved emotions, past experiences, or current stress. Sometimes, our minds and bodies respond to these pressures by making us feel down or overwhelmed.",
        " You might be going through a period of emotional turbulence, where things feel off. It’s important to reflect on any recent life changes or pressures that could be affecting your mood.",
        "Feeling like this consistently can sometimes indicate underlying mental health challenges, like anxiety or depression. It might be helpful to explore these feelings with a therapist or counselor.",
        "Physical health can also play a role. Lack of sleep, poor diet, or medical conditions might contribute to how you’re feeling emotionally and mentally. A check-up might give you some insights.",
        "Sometimes, when emotions pile up or go unexpressed, they can make us feel like we're in a constant state of sadness or frustration. It’s worth taking some time to explore and address what’s been going on internally.",
    ],
    r"is there something wrong with me?": [
        "There’s nothing wrong with you as a person. Everyone has struggles, and feeling low or anxious is part of being human. It doesn’t define your worth or who you are.",
        "It’s natural to feel this way when you're facing emotional difficulties. It doesn’t mean anything is fundamentally wrong with you; it just means you’re going through a tough time.",
        "Many people feel like this when they’re struggling with their mental health, but it’s important to remember that you are not broken. What you’re experiencing is common and treatable.",
        "Feeling like something is wrong is often a sign that your emotions need attention. Seeking support can help you better understand and manage these feelings.",
        "You're not alone in feeling this way. It’s okay to feel uncertain or question yourself, but it doesn’t mean there’s something inherently wrong with you. It’s part of life’s ups and downs.",
    ],
    r"Will I ever feel better again?": [
        "Yes, many people experience improvement over time, especially with the right support and treatment. Recovery is a process, and it’s okay to take it one step at a time.",
        "It’s essential to be patient with yourself. Healing can take time, but there is hope for brighter days ahead as you work through your feelings.",
        "Engaging in self-care practices, seeking therapy, and connecting with supportive friends or family can all contribute to feeling better over time.",
        "Remember that ups and downs are a natural part of life. While it may feel overwhelming now, things can change for the better with effort and support.",
        "You may find that as you address underlying issues and develop coping strategies, your overall mood and outlook improve significantly.",
    ],
    r"How long will therapy take to work?": [
        "The timeline for therapy varies for everyone. Some may see progress in a few sessions, while others might take several months to feel significant improvements.",
        "Factors such as the type of therapy, the issues being addressed, and your commitment to the process can all influence how quickly you see results.",
        "It’s important to communicate with your therapist about your goals and expectations. They can provide guidance on what to expect based on your specific situation.",
        "Therapy is often a journey rather than a quick fix. Staying consistent with your sessions and practicing skills learned in therapy can enhance your progress.",
        "Remember that progress is not always linear. There may be ups and downs along the way, but this doesn’t mean that therapy isn’t working.",
    ],
    r"Can depression be cured, or will I always have it?": [
        "Many people recover from depression completely, especially with the right treatment. For others, it may come and go, but with proper management, it becomes easier to handle over time.",
        "Depression can be treated very effectively, and many people experience long periods of remission. Even if it recurs, therapy and medication can help you manage it well.",
        "While depression might not always fully go away for everyone, many people learn to manage it successfully, and it can become much less intense or frequent with the right help.",
        "Some people recover from depression entirely, while others may experience it again in the future. The important thing is that it can be managed, and with time, most people find relief.",
        "Depression is treatable, and many people live fulfilling lives after overcoming it. For some, it may become a chronic condition, but with ongoing support, it doesn’t have to dominate your life.",
    ],
    r"Why do I keep pushing people away?": [
        "You might be pushing people away because you're afraid of getting hurt or being vulnerable. Sometimes, distancing ourselves feels like a way to protect ourselves from potential emotional pain.",
        "It could stem from past experiences where you’ve been let down or betrayed, making it difficult to trust others. Subconsciously, you may be trying to avoid repeating those feelings.",
        "Pushing people away can sometimes be a sign of low self-esteem. If you don’t feel deserving of love or support, you might withdraw before others have the chance to reject you.",
        "Fear of intimacy or commitment can lead to keeping people at arm’s length. This fear can make it hard to let others in, even when you want connection.",
        "You might be going through a period of emotional exhaustion, where social interactions feel draining. In this case, pushing people away might be a way to cope with overwhelming feelings.",
    ],
    r"Why do I always feel guilty, even when I haven’t done anything wrong?": [
        "You might be feeling guilt because of a tendency to be overly critical of yourself. High self-expectations can lead to guilt, even when there’s no actual wrongdoing.",
        "Sometimes, unresolved emotions or past experiences can leave you with a lingering sense of guilt. Even if you haven’t done anything wrong, these feelings can surface due to old habits or trauma.",
        "Guilt can stem from feeling responsible for others' emotions or outcomes. You may take on the burden of situations that aren’t entirely in your control, leading to unnecessary guilt.",
        "You might have grown up in an environment where you were often made to feel at fault, even for things outside your control. This can lead to a pattern of feeling guilty without clear cause.",
        "Anxiety can also manifest as feelings of guilt, even when there’s no logical reason. Your mind might be overanalyzing situations, making you feel like you've done something wrong when you haven’t.",
    ],
    r"How do I talk to my family about what I’m going through?": [
        "Choose a comfortable time and place where you can have an open and honest conversation without distractions. This setting can help create a supportive atmosphere for sharing your feelings.",
        "Start by expressing your feelings clearly. You might say something like, 'I’ve been feeling really overwhelmed lately, and I want to share what I’m going through.' This can help set the tone for the conversation.",
        "Be honest about your emotions, but also prepare for a range of reactions. Some family members may be understanding, while others may not know how to respond. It’s okay to guide the conversation back to your feelings if it strays.",
        "Use 'I' statements to express how you feel. For example, 'I feel sad when...' instead of 'You make me feel sad.' This can reduce defensiveness and promote better understanding.",
        "Be patient and give your family time to process what you share. They may need time to absorb the information and ask questions, so keeping the lines of communication open can foster a supportive environment.",
    ],
    r"What if therapy doesn’t work for me?": [
        "It’s important to remember that therapy is not a one-size-fits-all solution. If you feel it’s not working, consider discussing this with your therapist. They may adjust their approach or suggest alternative methods that might suit you better.",
        "Sometimes, it can take a few tries to find the right therapist or therapeutic approach that resonates with you. If one type of therapy isn’t effective, exploring different modalities, like cognitive-behavioral therapy (CBT) or mindfulness-based therapy, may yield better results.",
        "If traditional therapy isn’t helping, consider complementary approaches like support groups, medication, or holistic practices such as yoga or meditation. These can provide additional support and help manage your feelings.",
        "It’s normal to feel discouraged if you don’t see immediate results from therapy. Recovery is often a gradual process, and some people may experience ups and downs before finding a path that works for them.",
        "Remember that you are not alone in feeling this way. Many people face challenges with therapy, and seeking support from friends, family, or online communities can also be beneficial as you navigate your feelings and experiences.",
    ],
    r"Is medication the only solution?": [
        "No, medication is not the only solution for managing mental health issues. Many people benefit from a combination of therapies, lifestyle changes, and support systems alongside or instead of medication.",
        "Psychotherapy or counseling, such as cognitive-behavioral therapy (CBT) or dialectical behavior therapy (DBT), can be very effective for many individuals. These therapeutic approaches can help you develop coping skills and address underlying issues.",
        "Lifestyle changes, including regular exercise, a balanced diet, adequate sleep, and mindfulness practices, can significantly impact your mental health and may help reduce the need for medication.",
        "Support groups and community resources can also provide valuable support and help you connect with others facing similar challenges. Sharing experiences can be empowering and provide new perspectives on coping strategies.",
        "For some people, a holistic approach that includes alternative therapies like acupuncture, yoga, or art therapy can complement traditional treatment methods and enhance overall well-being. It’s essential to explore what works best for you.",
    ],
    r"How can I motivate myself to do even basic tasks?": [
        "Start small by breaking tasks into manageable steps. Focusing on completing just one small task can help build momentum and make larger tasks feel less overwhelming.",
        "Create a structured schedule to establish a routine. Setting specific times for tasks can help you develop consistency and make it easier to get started.",
        "Incorporate rewards for completing tasks, no matter how small. This positive reinforcement can motivate you to tackle more tasks over time.",
        "Practice self-compassion and recognize that it’s okay to have off days. Be gentle with yourself, and acknowledge your feelings instead of criticizing yourself for not accomplishing everything.",
        "Consider enlisting the support of friends or family. Sharing your goals with someone can create accountability and encouragement as you work through tasks.",
    ],
    r"Why do I feel so alone, even around people I care about?": [
        "Feeling alone in a crowd can stem from a disconnect between your inner feelings and your outward expressions. You might be surrounded by people but still feel emotionally distant or unable to share your true self.",
        "Sometimes, past experiences or unresolved emotions can create barriers to connection. If you’ve been hurt before, it can be hard to fully open up to those you care about, leading to feelings of isolation.",
        "Social anxiety or feelings of inadequacy can also contribute to this sense of loneliness. You might worry about how others perceive you, making it difficult to engage fully in social situations.",
        "It's possible to feel alone even when surrounded by loved ones if they don’t understand what you’re going through. If you haven’t communicated your feelings, they might not know how to support you.",
        "Feeling alone can sometimes be a sign that you’re longing for deeper connections. It’s natural to seek meaningful interactions, and if those needs aren’t being met, it can leave you feeling isolated even in the company of others.",
    ],
    r"What can I do to prevent a relapse if I start feeling better?": [
        "Maintain a routine: Establishing and sticking to a daily routine can provide structure and stability, helping you manage your mental health even when you’re feeling better. Incorporate self-care activities that promote well-being.",
        "Recognize triggers: Identify situations, thoughts, or feelings that have led to past relapses. By being aware of your triggers, you can develop strategies to cope with them when they arise.",
        "Stay connected: Keep in touch with supportive friends, family, or support groups. Maintaining these connections can provide encouragement and accountability during challenging times.",
        "Practice self-care: Continue prioritizing self-care practices, such as regular exercise, healthy eating, and mindfulness or relaxation techniques. These habits can help sustain your mental health and prevent a decline.",
        "Set realistic goals: While it’s great to feel better, be cautious about overextending yourself. Set achievable goals and be mindful of your limits to avoid becoming overwhelmed, which can lead to a relapse.",
    ],
    r"What if I never get over this?": [
        "It's natural to feel hopeless at times, but many people do find a way through their struggles. It's essential to keep in mind that feelings can change, and recovery is often a non-linear process.",
        "Consider focusing on small steps rather than the big picture. By setting manageable goals, you may find it easier to see progress and gain motivation as you move forward.",
        "Talking about your feelings with a trusted friend, family member, or therapist can provide perspective and support. They can help remind you that healing is possible and that you are not alone in your journey.",
        "Engaging in self-care and activities that bring you joy can help improve your mood and outlook over time. Finding fulfillment in small things can contribute to a sense of purpose.",
        "Remember that it’s okay to seek help when you’re feeling overwhelmed. Reaching out for support is a sign of strength, and many people find that talking about their experiences is a crucial part of healing.",
    ],
    r"Why do I feel so tired all the time?": [
        "Chronic fatigue can result from various factors, including inadequate sleep, stress, or underlying health conditions. It's important to evaluate your sleep patterns and overall lifestyle to identify possible causes.",
        "Emotional or mental exhaustion can also contribute to feelings of tiredness. If you're dealing with stress, anxiety, or depression, it can drain your energy levels, making you feel perpetually fatigued.",
        "Poor nutrition or dehydration can lead to fatigue as well. Ensuring you have a balanced diet and drink enough water can significantly impact your energy levels throughout the day.",
        "Sedentary lifestyles can contribute to tiredness. Engaging in regular physical activity, even light exercise, can boost your energy and improve your overall well-being.",
        "If you’ve made lifestyle changes but still feel fatigued, it might be worthwhile to consult a healthcare professional. They can help rule out any medical conditions that may be affecting your energy levels.",
    ],
    r"Why don’t I feel like doing anything anymore?": [
        "A loss of interest or motivation can be a symptom of depression or anxiety. When you're feeling overwhelmed or low, even enjoyable activities may seem unappealing.",
        "Burnout from stress or constant pressure can also lead to a lack of motivation. If you've been pushing yourself too hard, it’s natural to feel exhausted and disinterested in activities you once enjoyed.",
        "Changes in routine or life circumstances can impact your motivation. When faced with new challenges or disruptions, it can take time to adjust and find your motivation again.",
        "Low energy levels, whether physical or mental, can make it difficult to engage in activities. If you’re feeling fatigued, it can affect your desire to participate in everyday tasks.",
        "Consider taking small steps to re-engage with activities. Setting manageable goals and allowing yourself to take breaks can help gradually restore your motivation over time.",
    ],
}


# Resources
meditation_links = [
    {
        "title": "5 Minute Guided Meditation",
        "url": "https://www.youtube.com/watch?v=inpok4MKVLM",
    },
    {
        "title": "10 Minute Meditation for Anxiety",
        "url": "https://www.youtube.com/watch?v=O-6f5wQXSu8",
    },
    {
        "title": "Mindfulness Meditation to Start Your Day",
        "url": "https://www.youtube.com/watch?v=ZToicYcHIOU",
    },
]

mindfulness_quotes = [
    "Mindfulness is a way of befriending ourselves and our experience.",
    "The present moment is filled with joy and happiness. If you are attentive, you will see it.",
    "Do every act of your life as though it were the last act of your life.",
]

mindfulness_books = [
    {
        "title": "The Miracle of Mindfulness by Thich Nhat Hanh",
        "url": "https://amzn.to/3eUKP2A",
    },
    {"title": "The Power of Now by Eckhart Tolle", "url": "https://amzn.to/2TSrMjl"},
    {
        "title": "Wherever You Go, There You Are by Jon Kabat-Zinn",
        "url": "https://amzn.to/3gKBO6g",
    },
]

depression_books = [
    {"title": "Lost Connections by Johann Hari", "url": "https://amzn.to/3zMVJ4E"},
    {"title": "The Noonday Demon by Andrew Solomon", "url": "https://amzn.to/3qZlJDZ"},
]

breakup_books = [
    {
        "title": "Getting Past Your Breakup by Susan J. Elliott",
        "url": "https://amzn.to/3mOqWb8",
    },
    {
        "title": "How to Heal a Broken Heart in 30 Days by Howard Bronson",
        "url": "https://amzn.to/3Axk5hx",
    },
]


# Function to return resources
@app.route("/resources")
def get_resources():
    category = request.args.get("category")
    if category == "meditation":
        return jsonify(meditation_links)
    elif category == "quotes":
        return jsonify(mindfulness_quotes)
    elif category == "books_mindfulness":
        return jsonify(mindfulness_books)
    elif category == "books_depression":
        return jsonify(depression_books)
    elif category == "books_breakup":
        return jsonify(breakup_books)
    else:
        return jsonify({"error": "Invalid category"})


# Chatbot Response Function
last_bot_response = ""


def get_bot_response(user_input):
    global last_bot_response
    user_input = user_input.lower()
    response_found = False

    for pattern, responses in patterns_responses.items():
        match = re.search(pattern, user_input, re.IGNORECASE)
        if match:
            response = random.choice(responses).format(
                match.group(1) if match.groups() else ""
            )
            if response == last_bot_response:
                continue
            last_bot_response = response
            return response

    return "Could you please clarify that a bit more?"


# Routes
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get")
def get_bot_response_route():
    user_text = request.args.get("msg")
    return get_bot_response(user_text)


if __name__ == "__main__":
    app.run(debug=True)
