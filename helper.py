import re
from receipt_objects import ReceiptData 

def extract_json(text:str) -> str:
    text = re.sub(r'```json\s*', '', text)
    text = re.sub(r'```\s*$', '', text)

    start = text.find('{')
    end = text.rfind('}') + 1

    if start >= 0 and end > start:
        return text[start:end]
    
    return text.strip()

def format_results(receipt: ReceiptData) -> str:
        """Format results for display"""
        output = []
        output.append("🧾 RECEIPT ANALYSIS RESULTS")
        output.append("=" * 40)
        output.append(f"Merchant: {receipt.merchant_name}")
        if receipt.merchant_address:
            output.append(f"Address: {receipt.merchant_address}")
        output.append(f"Date: {receipt.date}")
        if receipt.time:
            output.append(f"Time: {receipt.time}")
        
        output.append("\n📝 ITEMS:")
        for i, item in enumerate(receipt.items, 1):
            output.append(f"{i}. {item.name}")
            output.append(f"   Qty: {item.quantity} × ${item.unit_price:.2f} = ${item.total_price:.2f}")
        
        output.append(f"\n💰 TOTALS:")
        output.append(f"Subtotal: ${receipt.subtotal:.2f}")
        output.append(f"Tax: ${receipt.tax_amount:.2f}")
        if receipt.tax_rate:
            output.append(f"Tax Rate: {receipt.tax_rate:.2f}%")
        output.append(f"TOTAL: ${receipt.total_amount:.2f}")
        
        if receipt.payment_method:
            output.append(f"Payment: {receipt.payment_method}")
        if receipt.receipt_number:
            output.append(f"Receipt #: {receipt.receipt_number}")
        
        return "\n".join(output)