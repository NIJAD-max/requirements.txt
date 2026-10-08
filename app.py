import streamlit as st

# ============================================================
# PAGE SETTINGS
# ============================================================

st.set_page_config(
    page_title="Library Management System",
    page_icon="📚",
    layout="wide"
)

# ============================================================
# SESSION STATE
# ============================================================

if "books" not in st.session_state:
    st.session_state.books = {}

if "members" not in st.session_state:
    st.session_state.members = {}

if "borrowed_books" not in st.session_state:
    st.session_state.borrowed_books = {}


books = st.session_state.books
members = st.session_state.members
borrowed_books = st.session_state.borrowed_books


# ============================================================
# TITLE
# ============================================================

st.title("📚 Library Management System")
st.write("Manage books, members and borrowing records easily.")

st.divider()


# ============================================================
# SIDEBAR MENU
# ============================================================

menu = st.sidebar.selectbox(
    "📋 Select Menu",
    [
        "🏠 Dashboard",
        "📖 Book Management",
        "👤 Member Management",
        "📕 Borrow Book",
        "📗 Return Book",
        "🔎 Search Book",
        "📊 Library Reports"
    ]
)


# ============================================================
# DASHBOARD
# ============================================================

if menu == "🏠 Dashboard":

    st.header("🏠 Library Dashboard")

    total_books = len(books)
    total_members = len(members)
    borrowed_count = len(borrowed_books)
    available_books = total_books - borrowed_count

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("📚 Total Books", total_books)

    with col2:
        st.metric("✅ Available Books", available_books)

    with col3:
        st.metric("📕 Borrowed Books", borrowed_count)

    with col4:
        st.metric("👤 Total Members", total_members)

    st.info("Use the menu on the left to manage the library.")


# ============================================================
# BOOK MANAGEMENT
# ============================================================

elif menu == "📖 Book Management":

    st.header("📖 Book Management")

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        [
            "➕ Add Book",
            "📚 View Books",
            "✏️ Edit Book",
            "🗑️ Delete Book",
            "🔎 Search Book"
        ]
    )

    # --------------------------------------------------------
    # ADD BOOK
    # --------------------------------------------------------

    with tab1:

        st.subheader("➕ Add New Book")

        book_id = st.text_input("Book ID")
        title = st.text_input("Book Title")
        author = st.text_input("Author Name")
        year = st.text_input("Publication Year")

        if st.button("Add Book", type="primary"):

            if not book_id or not title or not author or not year:
                st.warning("Please fill all fields.")

            elif book_id in books:
                st.error("Book ID already exists!")

            else:
                books[book_id] = {
                    "title": title,
                    "author": author,
                    "year": year,
                    "available": True
                }

                st.success("Book added successfully!")
                st.rerun()

    # --------------------------------------------------------
    # VIEW BOOKS
    # --------------------------------------------------------

    with tab2:

        st.subheader("📚 All Books")

        if not books:
            st.info("No books available.")

        else:

            for book_id, book in books.items():

                status = (
                    "🟢 Available"
                    if book["available"]
                    else "🔴 Borrowed"
                )

                with st.expander(
                    f"{book['title']} — ID: {book_id}"
                ):

                    st.write("**Book ID:**", book_id)
                    st.write("**Title:**", book["title"])
                    st.write("**Author:**", book["author"])
                    st.write("**Year:**", book["year"])
                    st.write("**Status:**", status)

    # --------------------------------------------------------
    # EDIT BOOK
    # --------------------------------------------------------

    with tab3:

        st.subheader("✏️ Edit Book")

        if not books:
            st.info("No books available.")

        else:

            edit_id = st.selectbox(
                "Select Book",
                list(books.keys())
            )

            book = books[edit_id]

            new_title = st.text_input(
                "Book Title",
                value=book["title"],
                key="edit_title"
            )

            new_author = st.text_input(
                "Author",
                value=book["author"],
                key="edit_author"
            )

            new_year = st.text_input(
                "Year",
                value=book["year"],
                key="edit_year"
            )

            if st.button("Update Book"):

                book["title"] = new_title
                book["author"] = new_author
                book["year"] = new_year

                st.success("Book updated successfully!")
                st.rerun()

    # --------------------------------------------------------
    # DELETE BOOK
    # --------------------------------------------------------

    with tab4:

        st.subheader("🗑️ Delete Book")

        if not books:
            st.info("No books available.")

        else:

            delete_id = st.selectbox(
                "Select Book to Delete",
                list(books.keys())
            )

            if not books[delete_id]["available"]:

                st.error(
                    "This book is currently borrowed and cannot be deleted."
                )

            else:

                confirm = st.checkbox(
                    "I confirm that I want to delete this book."
                )

                if st.button("Delete Book"):

                    if confirm:

                        del books[delete_id]

                        st.success("Book deleted successfully!")
                        st.rerun()

                    else:

                        st.warning(
                            "Please confirm deletion."
                        )

    # --------------------------------------------------------
    # SEARCH BOOK
    # --------------------------------------------------------

    with tab5:

        st.subheader("🔎 Search Book")

        search = st.text_input(
            "Enter book title or author"
        ).lower()

        if search:

            found = False

            for book_id, book in books.items():

                if (
                    search in book["title"].lower()
                    or search in book["author"].lower()
                ):

                    found = True

                    status = (
                        "Available"
                        if book["available"]
                        else "Borrowed"
                    )

                    st.write("---")
                    st.write("**Book ID:**", book_id)
                    st.write("**Title:**", book["title"])
                    st.write("**Author:**", book["author"])
                    st.write("**Year:**", book["year"])
                    st.write("**Status:**", status)

            if not found:
                st.warning("No matching book found.")


# ============================================================
# MEMBER MANAGEMENT
# ============================================================

elif menu == "👤 Member Management":

    st.header("👤 Member Management")

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "➕ Add Member",
            "👥 View Members",
            "✏️ Edit Member",
            "🗑️ Delete Member"
        ]
    )

    # --------------------------------------------------------
    # ADD MEMBER
    # --------------------------------------------------------

    with tab1:

        st.subheader("➕ Add Member")

        member_id = st.text_input("Member ID")
        name = st.text_input("Member Name")
        phone = st.text_input("Phone Number")

        if st.button("Add Member", type="primary"):

            if not member_id or not name or not phone:

                st.warning("Please fill all fields.")

            elif member_id in members:

                st.error("Member ID already exists!")

            else:

                members[member_id] = {
                    "name": name,
                    "phone": phone
                }

                st.success("Member added successfully!")
                st.rerun()

    # --------------------------------------------------------
    # VIEW MEMBERS
    # --------------------------------------------------------

    with tab2:

        st.subheader("👥 All Members")

        if not members:

            st.info("No members registered.")

        else:

            for member_id, member in members.items():

                with st.expander(
                    f"{member['name']} — ID: {member_id}"
                ):

                    st.write("**Member ID:**", member_id)
                    st.write("**Name:**", member["name"])
                    st.write("**Phone:**", member["phone"])

    # --------------------------------------------------------
    # EDIT MEMBER
    # --------------------------------------------------------

    with tab3:

        st.subheader("✏️ Edit Member")

        if not members:

            st.info("No members registered.")

        else:

            edit_member_id = st.selectbox(
                "Select Member",
                list(members.keys())
            )

            member = members[edit_member_id]

            new_name = st.text_input(
                "Member Name",
                value=member["name"],
                key="new_member_name"
            )

            new_phone = st.text_input(
                "Phone Number",
                value=member["phone"],
                key="new_member_phone"
            )

            if st.button("Update Member"):

                member["name"] = new_name
                member["phone"] = new_phone

                st.success("Member updated successfully!")
                st.rerun()

    # --------------------------------------------------------
    # DELETE MEMBER
    # --------------------------------------------------------

    with tab4:

        st.subheader("🗑️ Delete Member")

        if not members:

            st.info("No members registered.")

        else:

            delete_member_id = st.selectbox(
                "Select Member to Delete",
                list(members.keys())
            )

            has_borrowed = False

            for record in borrowed_books.values():

                if record["member_id"] == delete_member_id:
                    has_borrowed = True

            if has_borrowed:

                st.error(
                    "This member currently has a borrowed book. "
                    "Return the book before deleting the member."
                )

            else:

                confirm = st.checkbox(
                    "I confirm that I want to delete this member."
                )

                if st.button("Delete Member"):

                    if confirm:

                        del members[delete_member_id]

                        st.success(
                            "Member deleted successfully!"
                        )

                        st.rerun()

                    else:

                        st.warning(
                            "Please confirm deletion."
                        )


# ============================================================
# BORROW BOOK
# ============================================================

elif menu == "📕 Borrow Book":

    st.header("📕 Borrow Book")

    if not books:

        st.warning("No books available.")

    elif not members:

        st.warning("No members registered.")

    else:

        available_ids = [
            book_id
            for book_id, book in books.items()
            if book["available"]
        ]

        if not available_ids:

            st.info("No books are currently available.")

        else:

            book_id = st.selectbox(
                "Select Book",
                available_ids,
                format_func=lambda x:
                f"{x} - {books[x]['title']}"
            )

            member_id = st.selectbox(
                "Select Member",
                list(members.keys()),
                format_func=lambda x:
                f"{x} - {members[x]['name']}"
            )

            if st.button("📕 Borrow Book", type="primary"):

                books[book_id]["available"] = False

                borrowed_books[book_id] = {
                    "member_id": member_id
                }

                st.success(
                    f"'{books[book_id]['title']}' "
                    f"borrowed by {members[member_id]['name']}."
                )

                st.rerun()


# ============================================================
# RETURN BOOK
# ============================================================

elif menu == "📗 Return Book":

    st.header("📗 Return Book")

    if not borrowed_books:

        st.info("No books are currently borrowed.")

    else:

        book_id = st.selectbox(
            "Select Borrowed Book",
            list(borrowed_books.keys()),
            format_func=lambda x:
            f"{x} - {books[x]['title']}"
        )

        member_id = borrowed_books[book_id]["member_id"]

        st.write(
            "**Borrowed by:**",
            members[member_id]["name"]
        )

        if st.button("📗 Return Book", type="primary"):

            books[book_id]["available"] = True

            del borrowed_books[book_id]

            st.success("Book returned successfully!")

            st.rerun()


# ============================================================
# SEARCH BOOK
# ============================================================

elif menu == "🔎 Search Book":

    st.header("🔎 Search Book")

    search = st.text_input(
        "Search by book title or author"
    ).lower()

    if search:

        found = False

        for book_id, book in books.items():

            if (
                search in book["title"].lower()
                or search in book["author"].lower()
            ):

                found = True

                status = (
                    "🟢 Available"
                    if book["available"]
                    else "🔴 Borrowed"
                )

                st.success(
                    f"📖 {book['title']} "
                    f"(ID: {book_id})"
                )

                st.write("Author:", book["author"])
                st.write("Year:", book["year"])
                st.write("Status:", status)

        if not found:

            st.warning("No matching book found.")


# ============================================================
# LIBRARY REPORTS
# ============================================================

elif menu == "📊 Library Reports":

    st.header("📊 Library Reports")

    total_books = len(books)
    total_members = len(members)
    borrowed_count = len(borrowed_books)
    available_books = total_books - borrowed_count

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("📚 Total Books", total_books)

    with col2:
        st.metric("🟢 Available", available_books)

    with col3:
        st.metric("🔴 Borrowed", borrowed_count)

    with col4:
        st.metric("👥 Members", total_members)

    st.divider()

    st.subheader("📕 Borrowing Records")

    if not borrowed_books:

        st.info("No books are currently borrowed.")

    else:

        for book_id, record in borrowed_books.items():

            member_id = record["member_id"]

            st.write("---")

            col1, col2 = st.columns(2)

            with col1:
                st.write("**Book ID:**", book_id)
                st.write(
                    "**Book Name:**",
                    books[book_id]["title"]
                )

            with col2:
                st.write("**Member ID:**", member_id)
                st.write(
                    "**Member Name:**",
                    members[member_id]["name"]
                )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption("📚 Library Management System | Built with Python & Streamlit")
