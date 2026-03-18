import re
import unicodedata
import contractions


sample_text = """drug developers switch gears to a wide variety of flavors of software and services as a function of the technology 

The current state of blockchain-based cryptocurrencies is changing the way startups and enterprises deal with innovation and disrupt themselves. There are dozens of different projects currently out there, and with blockchain becoming more and more mainstream, it’s only a matter of time that we get access to blockchain based cryptocurrency exchanges, or ‘solutions’. Many of which are still in development and a few of which have only just made it to production. If you’re building anything for the blockchain age, there is literally nothing better than a blockchain-based exchange. Not only does this ensure a faster and more accurate exchange, but it also reduces fees that can significantly increase the value of an asset.

In this article we’ll describe three: Poloniex, Bittrex and Kraken. All three are well-known exchanges with a blockchain wallet for every cryptocurrency you may use, and if you want to trade them in a single click, they are your single best option."""
    

# -----------------------------
# Current method: OpenVocab only
# -----------------------------
class OpenVocab:
    def process(self, data: str):
        return self.split_by_space(
            self.expand_contractions(
                self.remove_punctuation(
                    self.remove_non_ascii(
                        self.lower_case(data)
                    )
                )
            )
        )

    def lower_case(self, data: str):
        return data.lower()

    def remove_non_ascii(self, data: str):
        return unicodedata.normalize('NFKD', data).encode('ascii', 'ignore').decode('utf-8', 'ignore')

    def remove_punctuation(self, data: str):
        data = re.sub(r"[.\']", "", data)
        return re.sub(r"[^\w\s]|_", " ", data).strip()

    def expand_contractions(self, text: str):
        return contractions.fix(text)

    def split_by_space(self, data: str):
        return data.split()


# -----------------------------
# Old method
# -----------------------------
def old_process_data(data: str):
    normalized_data = unicodedata.normalize('NFKD', data).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    normalized_data = normalized_data.lower()
    normalized_data = re.sub(r"[^\w\s]", "", normalized_data).strip()
    tokens = normalized_data.split()
    return tokens


# -----------------------------
# Run both methods
# -----------------------------
open_processor = OpenVocab()

open_tokens = open_processor.process(sample_text)
old_tokens = old_process_data(sample_text)

print("=== CURRENT METHOD (OpenVocab) ===")
print(open_tokens)
print("\nToken count:", len(open_tokens))

print("\n=== OLD METHOD ===")
print(old_tokens)
print("\nToken count:", len(old_tokens))