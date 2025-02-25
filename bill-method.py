import streamlit as st
from datetime import datetime

# **Session state initialization**
if "sales_data" not in st.session_state:
    st.session_state.sales_data = []  # Stores all sales records

# **Title of the application**
st.title("Master Food Bill Generator")

# **Input fields for Date and Time**
col1, col2 = st.columns(2)
with col1:
    date = st.date_input("Date", datetime.now())
with col2:
    time = st.time_input("Time", datetime.now().time())

# **Dictionary of menu items with prices**
menu = {
    "Cheese Burger": 150,
    "Chicken Burger": 200,
    "Veggie Burger": 130,
    "French Fries": 100,
    "Coke": 50
}

st.write("### Select Items and Quantity:")

# **Store selected items with quantity**
selected_items = []
total_bill = 0  

# **Creating checkboxes with quantity inputs**
for item, price in menu.items():
    col1, col2 = st.columns([2, 1])
    with col1:
        selected = st.checkbox(f"{item} - Rs. {price}", key=f"chk_{item}")
    with col2:
        quantity = st.number_input(f"Qty ({item})", min_value=1, max_value=10, value=1, key=f"qty_{item}") if selected else 0
    
    if selected and quantity > 0:
        total_price = price * quantity
        selected_items.append((item, price, quantity, total_price))
        total_bill += total_price

# **Bill Generation Button**
if st.button("Generate Bill"):
    if not selected_items:
        st.warning("⚠️ No items selected. Please select items to generate a bill.")
    else:
        # **Store sale in session state**
        for item, price, qty, total in selected_items:
            st.session_state.sales_data.append({
                "Date": date,
                "Time": time,
                "Item": item,
                "Quantity Sold": qty,
                "Total Revenue": total
            })
        st.success("✅ Bill generated successfully!")

# **Multi-page bill selection**
page = st.radio("📄 Select Bill Page", ["📝 Order Summary", "📊 Sales Report", "🧾 Customer Receipt"])

# ✅ **Common Print JavaScript**
print_script = """
<script>
function printOrder(divId) {
    var divContents = document.getElementById(divId).innerHTML;
    var a = window.open('', '', 'height=500, width=500');
    a.document.write('<html><head><title>Print</title></head>');
    a.document.write('<body >');
    a.document.write(divContents);
    a.document.write('</body></html>');
    a.document.close();
    a.print();
}
</script>
"""

# **Page 1: Order Summary**
if page == "📝 Order Summary":
    st.write("## 🧾 Order Summary")
    st.write(f"**📅 Date:** {date}")
    st.write(f"**⏰ Time:** {time}")
    
    if selected_items:
        bill_data = [{"Item": item, "Price (Rs.)": price, "Quantity": qty, "Total (Rs.)": total} for item, price, qty, total in selected_items]
        st.table(bill_data)
        st.write(f"## **💰 Grand Total: Rs. {total_bill}**")

        # ✅ Add Print Button for Order Summary
        st.markdown(print_script, unsafe_allow_html=True)
        st.markdown('<div id="order_summary">', unsafe_allow_html=True)
        st.write(bill_data)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<button onclick="printOrder(\'order_summary\')">🖨️ Print Order</button>', unsafe_allow_html=True)

    else:
        st.warning("⚠️ No items selected.")

# **Page 2: Sales Report (Persistent Data)**
elif page == "📊 Sales Report":
    st.write("## 📊 Sales Report")
    
    if st.session_state.sales_data:
        total_items_sold = sum(entry["Quantity Sold"] for entry in st.session_state.sales_data)
        total_revenue = sum(entry["Total Revenue"] for entry in st.session_state.sales_data)
        
        st.write(f"📦 **Total Items Sold:** {total_items_sold}")
        st.write(f"💵 **Total Revenue:** Rs. {total_revenue}")
        
        st.table(st.session_state.sales_data)
    else:
        st.warning("⚠️ No sales data available.")

# **Page 3: Customer Receipt**
elif page == "🧾 Customer Receipt":
    st.write("## 🧾 Customer Receipt")
    st.write(f"**📅 Date:** {date}")
    st.write(f"**⏰ Time:** {time}")
    st.write("---")
    
    if selected_items:
        st.markdown('<div id="customer_receipt">', unsafe_allow_html=True)
        
        for item, price, qty, total in selected_items:
            st.write(f"🛒 {item} x {qty} = Rs. {total}")
        
        st.write("---")
        st.write(f"### **Total Amount Paid: Rs. {total_bill}**")
        st.success("🎉 Thank you for your purchase!")
        
        st.markdown('</div>', unsafe_allow_html=True)

        # ✅ Add Print Button for Customer Receipt
        st.markdown(print_script, unsafe_allow_html=True)
        st.markdown('<button onclick="printOrder(\'customer_receipt\')">🖨️ Print Receipt</button>', unsafe_allow_html=True)
    
    else:
        st.warning("⚠️ No items purchased.")
