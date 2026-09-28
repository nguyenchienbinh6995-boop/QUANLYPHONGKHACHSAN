import streamlit as st
import pandas as pd
from datetime import date, datetime

# ============================================================
# CẤU HÌNH APP
# ============================================================

st.set_page_config(
    page_title="Hotel Management System",
    page_icon="🏨",
    layout="wide"
)

# ============================================================
# DỮ LIỆU MẪU
# ============================================================

ROOM_DATA = [
    {
        "room_id": "101",
        "room_type": "Standard",
        "capacity": 2,
        "price": 800000,
        "status": "Trống",
        "guest": ""
    },
    {
        "room_id": "102",
        "room_type": "Standard",
        "capacity": 2,
        "price": 800000,
        "status": "Đang ở",
        "guest": "Nguyễn Văn An"
    },
    {
        "room_id": "103",
        "room_type": "Deluxe",
        "capacity": 2,
        "price": 1200000,
        "status": "Trống",
        "guest": ""
    },
    {
        "room_id": "104",
        "room_type": "Deluxe",
        "capacity": 3,
        "price": 1500000,
        "status": "Đang dọn",
        "guest": ""
    },
    {
        "room_id": "201",
        "room_type": "Suite",
        "capacity": 4,
        "price": 2500000,
        "status": "Trống",
        "guest": ""
    },
    {
        "room_id": "202",
        "room_type": "Suite",
        "capacity": 4,
        "price": 2500000,
        "status": "Bảo trì",
        "guest": ""
    },
    {
        "room_id": "203",
        "room_type": "Family",
        "capacity": 5,
        "price": 3000000,
        "status": "Trống",
        "guest": ""
    },
]

BOOKING_DATA = [
    {
        "booking_id": "BK001",
        "guest_name": "Nguyễn Văn An",
        "phone": "0901234567",
        "room_id": "102",
        "room_type": "Standard",
        "check_in": date(2026, 9, 27),
        "check_out": date(2026, 9, 30),
        "guests": 2,
        "status": "Đã nhận phòng",
        "created_at": "27/09/2026 14:00"
    }
]

# ============================================================
# SESSION STATE
# ============================================================

if "rooms" not in st.session_state:
    st.session_state.rooms = pd.DataFrame(ROOM_DATA)

if "bookings" not in st.session_state:
    st.session_state.bookings = pd.DataFrame(BOOKING_DATA)


# ============================================================
# HÀM TIỆN ÍCH
# ============================================================

def format_price(value):
    return f"{value:,.0f} VNĐ"


def status_icon(status):
    icons = {
        "Trống": "🟢",
        "Đang ở": "🔴",
        "Đang dọn": "🟡",
        "Bảo trì": "⚫"
    }

    return icons.get(status, "⚪")


def calculate_nights(check_in, check_out):
    return (check_out - check_in).days


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🏨 HOTEL MANAGEMENT")

st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Chọn chức năng",
    [
        "🛏️ Quản lý phòng",
        "📋 Quản lý đặt phòng"
    ]
)

st.sidebar.markdown("---")

st.sidebar.info(
    "Hệ thống quản lý khách sạn\n\n"
    "Phiên bản MVP\n"
    "Streamlit + Pandas"
)


# ============================================================
# PHẦN 1: QUẢN LÝ PHÒNG
# ============================================================

if menu == "🛏️ Quản lý phòng":

    st.title("🛏️ QUẢN LÝ PHÒNG KHÁCH SẠN")

    st.write(
        "Theo dõi tình trạng phòng, loại phòng, khách đang ở "
        "và cập nhật trạng thái phòng."
    )

    st.markdown("---")

    # --------------------------------------------------------
    # THỐNG KÊ
    # --------------------------------------------------------

    rooms = st.session_state.rooms

    total_rooms = len(rooms)
    available_rooms = len(
        rooms[rooms["status"] == "Trống"]
    )
    occupied_rooms = len(
        rooms[rooms["status"] == "Đang ở"]
    )
    cleaning_rooms = len(
        rooms[rooms["status"] == "Đang dọn"]
    )
    maintenance_rooms = len(
        rooms[rooms["status"] == "Bảo trì"]
    )

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric(
        "Tổng phòng",
        total_rooms
    )

    col2.metric(
        "🟢 Trống",
        available_rooms
    )

    col3.metric(
        "🔴 Đang ở",
        occupied_rooms
    )

    col4.metric(
        "🟡 Đang dọn",
        cleaning_rooms
    )

    col5.metric(
        "⚫ Bảo trì",
        maintenance_rooms
    )

    st.markdown("---")

    # --------------------------------------------------------
    # BỘ LỌC
    # --------------------------------------------------------

    st.subheader("🔎 Tìm kiếm phòng")

    col1, col2, col3 = st.columns(3)

    with col1:
        search_room = st.text_input(
            "Số phòng",
            placeholder="Ví dụ: 101"
        )

    with col2:
        room_type_filter = st.selectbox(
            "Loại phòng",
            [
                "Tất cả",
                "Standard",
                "Deluxe",
                "Suite",
                "Family"
            ]
        )

    with col3:
        status_filter = st.selectbox(
            "Trạng thái",
            [
                "Tất cả",
                "Trống",
                "Đang ở",
                "Đang dọn",
                "Bảo trì"
            ]
        )

    filtered_rooms = rooms.copy()

    if search_room:
        filtered_rooms = filtered_rooms[
            filtered_rooms["room_id"]
            .astype(str)
            .str.contains(search_room)
        ]

    if room_type_filter != "Tất cả":
        filtered_rooms = filtered_rooms[
            filtered_rooms["room_type"]
            == room_type_filter
        ]

    if status_filter != "Tất cả":
        filtered_rooms = filtered_rooms[
            filtered_rooms["status"]
            == status_filter
        ]

    # --------------------------------------------------------
    # HIỂN THỊ DANH SÁCH PHÒNG
    # --------------------------------------------------------

    st.subheader("📋 Danh sách phòng")

    display_rooms = filtered_rooms.copy()

    display_rooms["Trạng thái"] = display_rooms[
        "status"
    ].apply(
        lambda x: f"{status_icon(x)} {x}"
    )

    display_rooms["Giá phòng"] = display_rooms[
        "price"
    ].apply(format_price)

    display_rooms = display_rooms[
        [
            "room_id",
            "room_type",
            "capacity",
            "Giá phòng",
            "Trạng thái",
            "guest"
        ]
    ]

    display_rooms.columns = [
        "Số phòng",
        "Loại phòng",
        "Sức chứa",
        "Giá",
        "Trạng thái",
        "Khách"
    ]

    st.dataframe(
        display_rooms,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")

    # --------------------------------------------------------
    # CẬP NHẬT PHÒNG
    # --------------------------------------------------------

    st.subheader("⚙️ Cập nhật trạng thái phòng")

    col1, col2, col3 = st.columns(3)

    with col1:
        selected_room = st.selectbox(
            "Chọn phòng",
            rooms["room_id"].tolist()
        )

    current_room = rooms[
        rooms["room_id"] == selected_room
    ].iloc[0]

    with col2:
        new_status = st.selectbox(
            "Trạng thái mới",
            [
                "Trống",
                "Đang ở",
                "Đang dọn",
                "Bảo trì"
            ],
            index=[
                "Trống",
                "Đang ở",
                "Đang dọn",
                "Bảo trì"
            ].index(current_room["status"])
        )

    with col3:
        guest_name = st.text_input(
            "Tên khách",
            value=current_room["guest"]
        )

    if st.button(
        "💾 Cập nhật phòng",
        use_container_width=True
    ):

        index = rooms[
            rooms["room_id"] == selected_room
        ].index[0]

        st.session_state.rooms.loc[
            index, "status"
        ] = new_status

        if new_status == "Đang ở":
            st.session_state.rooms.loc[
                index, "guest"
            ] = guest_name
        else:
            st.session_state.rooms.loc[
                index, "guest"
            ] = ""

        st.success(
            f"Đã cập nhật phòng {selected_room}"
        )

        st.rerun()


# ============================================================
# PHẦN 2: QUẢN LÝ ĐẶT PHÒNG
# ============================================================

elif menu == "📋 Quản lý đặt phòng":

    st.title("📋 QUẢN LÝ ĐẶT PHÒNG")

    st.write(
        "Tạo đặt phòng, kiểm tra booking, "
        "check-in, check-out và hủy đặt phòng."
    )

    st.markdown("---")

    bookings = st.session_state.bookings
    rooms = st.session_state.rooms

    # --------------------------------------------------------
    # THỐNG KÊ BOOKING
    # --------------------------------------------------------

    total_bookings = len(bookings)

    pending_bookings = len(
        bookings[
            bookings["status"] == "Đã đặt"
        ]
    )

    checked_in = len(
        bookings[
            bookings["status"] == "Đã nhận phòng"
        ]
    )

    checked_out = len(
        bookings[
            bookings["status"] == "Đã trả phòng"
        ]
    )

    cancelled = len(
        bookings[
            bookings["status"] == "Đã hủy"
        ]
    )

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric(
        "Tổng booking",
        total_bookings
    )

    col2.metric(
        "Đã đặt",
        pending_bookings
    )

    col3.metric(
        "Đang ở",
        checked_in
    )

    col4.metric(
        "Đã trả phòng",
        checked_out
    )

    col5.metric(
        "Đã hủy",
        cancelled
    )

    st.markdown("---")

    # --------------------------------------------------------
    # TẠO BOOKING
    # --------------------------------------------------------

    st.subheader("➕ Tạo đặt phòng mới")

    available_rooms = rooms[
        rooms["status"] == "Trống"
    ]

    if len(available_rooms) == 0:

        st.warning(
            "Hiện tại không có phòng trống."
        )

    else:

        with st.form("booking_form"):

            col1, col2 = st.columns(2)

            with col1:

                guest_name = st.text_input(
                    "Họ và tên khách *"
                )

                phone = st.text_input(
                    "Số điện thoại *"
                )

                number_of_guests = st.number_input(
                    "Số khách",
                    min_value=1,
                    max_value=20,
                    value=2
                )

                selected_room = st.selectbox(
                    "Chọn phòng *",
                    available_rooms["room_id"].tolist()
                )

            with col2:

                check_in = st.date_input(
                    "Ngày nhận phòng",
                    value=date.today()
                )

                check_out = st.date_input(
                    "Ngày trả phòng",
                    value=date.today()
                )

                note = st.text_area(
                    "Ghi chú",
                    placeholder="Yêu cầu đặc biệt của khách..."
                )

            submitted = st.form_submit_button(
                "➕ Tạo booking",
                use_container_width=True
            )

            if submitted:

                if not guest_name:
                    st.error(
                        "Vui lòng nhập tên khách."
                    )

                elif not phone:
                    st.error(
                        "Vui lòng nhập số điện thoại."
                    )

                elif check_out <= check_in:
                    st.error(
                        "Ngày trả phòng phải sau ngày nhận phòng."
                    )

                else:

                    selected_room_data = rooms[
                        rooms["room_id"] == selected_room
                    ].iloc[0]

                    new_booking_id = (
                        f"BK{len(bookings) + 1:03d}"
                    )

                    new_booking = {
                        "booking_id": new_booking_id,
                        "guest_name": guest_name,
                        "phone": phone,
                        "room_id": selected_room,
                        "room_type": selected_room_data[
                            "room_type"
                        ],
                        "check_in": check_in,
                        "check_out": check_out,
                        "guests": number_of_guests,
                        "status": "Đã đặt",
                        "created_at": datetime.now().strftime(
                            "%d/%m/%Y %H:%M"
                        )
                    }

                    st.session_state.bookings = pd.concat(
                        [
                            bookings,
                            pd.DataFrame([new_booking])
                        ],
                        ignore_index=True
                    )

                    st.success(
                        f"Đã tạo booking {new_booking_id}"
                    )

                    st.rerun()

    st.markdown("---")

    # --------------------------------------------------------
    # DANH SÁCH BOOKING
    # --------------------------------------------------------

    st.subheader("📑 Danh sách đặt phòng")

    if len(bookings) == 0:

        st.info(
            "Chưa có booking nào."
        )

    else:

        display_bookings = bookings.copy()

        display_bookings[
            "Check-in"
        ] = display_bookings[
            "check_in"
        ].apply(
            lambda x: x.strftime("%d/%m/%Y")
        )

        display_bookings[
            "Check-out"
        ] = display_bookings[
            "check_out"
        ].apply(
            lambda x: x.strftime("%d/%m/%Y")
        )

        display_bookings = display_bookings[
            [
                "booking_id",
                "guest_name",
                "phone",
                "room_id",
                "room_type",
                "Check-in",
                "Check-out",
                "guests",
                "status"
            ]
        ]

        display_bookings.columns = [
            "Booking",
            "Khách hàng",
            "Điện thoại",
            "Phòng",
            "Loại phòng",
            "Check-in",
            "Check-out",
            "Số khách",
            "Trạng thái"
        ]

        st.dataframe(
            display_bookings,
            use_container_width=True,
            hide_index=True
        )

    st.markdown("---")

    # --------------------------------------------------------
    # XỬ LÝ BOOKING
    # --------------------------------------------------------

    st.subheader("🔧 Xử lý booking")

    if len(bookings) > 0:

        selected_booking = st.selectbox(
            "Chọn booking",
            bookings["booking_id"].tolist()
        )

        booking_index = bookings[
            bookings["booking_id"] == selected_booking
        ].index[0]

        selected_booking_data = bookings.loc[
            booking_index
        ]

        st.write(
            f"**Khách:** "
            f"{selected_booking_data['guest_name']}"
        )

        st.write(
            f"**Phòng:** "
            f"{selected_booking_data['room_id']}"
        )

        st.write(
            f"**Trạng thái hiện tại:** "
            f"{selected_booking_data['status']}"
        )

        col1, col2, col3 = st.columns(3)

        current_status = selected_booking_data["status"]

        # ----------------------------------------------------
        # CHECK-IN
        # ----------------------------------------------------

        with col1:

            if st.button(
                "🟢 Check-in",
                use_container_width=True,
                disabled=current_status != "Đã đặt"
            ):

                room_id = selected_booking_data[
                    "room_id"
                ]

                # Cập nhật booking
                st.session_state.bookings.loc[
                    booking_index,
                    "status"
                ] = "Đã nhận phòng"

                # Cập nhật phòng
                room_index = rooms[
                    rooms["room_id"] == room_id
                ].index[0]

                st.session_state.rooms.loc[
                    room_index,
                    "status"
                ] = "Đang ở"

                st.session_state.rooms.loc[
                    room_index,
                    "guest"
                ] = selected_booking_data[
                    "guest_name"
                ]

                st.success(
                    f"Check-in thành công phòng {room_id}"
                )

                st.rerun()

        # ----------------------------------------------------
        # CHECK-OUT
        # ----------------------------------------------------

        with col2:

            if st.button(
                "🔵 Check-out",
                use_container_width=True,
                disabled=current_status != "Đã nhận phòng"
            ):

                room_id = selected_booking_data[
                    "room_id"
                ]

                st.session_state.bookings.loc[
                    booking_index,
                    "status"
                ] = "Đã trả phòng"

                room_index = rooms[
                    rooms["room_id"] == room_id
                ].index[0]

                st.session_state.rooms.loc[
                    room_index,
                    "status"
                ] = "Đang dọn"

                st.session_state.rooms.loc[
                    room_index,
                    "guest"
                ] = ""

                st.success(
                    f"Check-out thành công phòng {room_id}"
                )

                st.rerun()

        # ----------------------------------------------------
        # HỦY BOOKING
        # ----------------------------------------------------

        with col3:

            if st.button(
                "❌ Hủy booking",
                use_container_width=True,
                disabled=current_status != "Đã đặt"
            ):

                st.session_state.bookings.loc[
                    booking_index,
                    "status"
                ] = "Đã hủy"

                st.warning(
                    f"Đã hủy booking {selected_booking}"
                )

                st.rerun()
