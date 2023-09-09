# Lexing Multi-character operators

Sometimes, you can't parse a token based on its first character
- there could be mulitple operators with the same starting character, but different later characters
- for example, `=` and `==`, or `!` and `!=`

The appropriate way to deal with this is "peeking"
- this is similar to reading the next character, but you don't move the character pointer forward
