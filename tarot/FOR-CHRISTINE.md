# Publishing Lantern Tarot under your own Claude account

This takes about five minutes and you only do it once. Afterwards the app is yours: readings run on your own Claude, and your journal and daily cards live on your phone.

1. On a computer, go to https://claude.ai/code and sign in to your Claude account. If it asks you to connect GitHub and choose a repository, connect a GitHub account (a free one is fine) and pick any repository. The repository is only needed to start a session; the app does not come from it.
2. Start a new session and paste this message, exactly:

```
Download this file with curl, without changing it, then publish it as an Artifact:
https://raw.githubusercontent.com/justingordon2016-max/Personal-finance-/claude/tarot-reading-app-u9n1l1/tarot/artifact.html

Publish it with the title "Lantern Tarot", the favicon 🏮, and the runtime capability `sample` enabled (capabilities: {"sample": {}}), so the page can ask Claude for readings. Do not edit the file. Give me the artifact link when it is published.
```

3. Claude will reply with a link. Open it on your phone in Safari or Chrome while signed in to your Claude account.
4. Tap Share, then Add to Home Screen.
5. The first time you lay a reading, it asks permission for the page to use your Claude. Allow it, once.

That is all. The link is private to your account.
