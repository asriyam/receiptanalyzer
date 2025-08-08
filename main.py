import helper
from analyzer import ReceiptAnalyzer
from dotenv import load_dotenv

load_dotenv()

analyzer = ReceiptAnalyzer()
image_path = "wallmart.jpeg"

print("Starting receipt analysis ")
result = analyzer.analyze_receipt(image_path)

if result:
    print(helper.format_results(result))
else:
    print("Failed to analyze receipt")
