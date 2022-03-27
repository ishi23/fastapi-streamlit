import streamlit as st
import random
import requests
import json
import datetime
import pandas as pd

api_base_url = "http://127.0.0.1:8000/"

page = st.sidebar.selectbox("Choose Your Page", ["users", "rooms", "bookings"])

if page == "users":

    st.title("ユーザー登録画面")

    # withでFormを括る
    with st.form(key="user"):
        # user_id: int = random.randint(0, 10)
        username: str = st.text_input("ユーザー名", max_chars=12)
        data = {
            # "user_id": user_id,
            "username": username
        }
        submit_botton = st.form_submit_button(label="リクエスト送信")

    if submit_botton:
        st.write("## レスポンス結果")
        url = api_base_url + "users/"
        res = requests.post(
            url,
            data = json.dumps(data)
        )
        st.write(res.status_code)
        if res.status_code == 200:
            st.success("ユーザー登録完了")
        st.json(res.json())


elif page == "rooms":

    st.title("会議室登録画面")

    # withでFormを括る
    with st.form(key="room"):
        # room_id: int = random.randint(0, 10)
        room_name: str = st.text_input("会議室名", max_chars=12)
        capacity: int = st.number_input("定員", step=1)
        data = {
            # "room_id": room_id,
            "room_name": room_name,
            "capacity": capacity
        }
        submit_botton = st.form_submit_button(label="会議室登録")

    if submit_botton:
        st.write("## レスポンス結果")
        url = api_base_url + "rooms"
        res = requests.post(
            url,
            data = json.dumps(data)
        )
        st.write(res.status_code)
        if res.status_code == 200:
            st.success("会議室登録完了")
        st.json(res.json())


elif page == "bookings":

    st.title("会議室予約画面")

    # ユーザー一覧取得
    url_users = api_base_url + "users/"
    users = requests.get(url_users).json()
    # st.json(users)
    users_name = {}
    for user in users:
        users_name[user["username"]] = user["user_id"]
    # st.write(users_name)

    # 会議室一覧取得
    url_rooms = api_base_url + "rooms/"
    rooms = requests.get(url_rooms).json()
    # st.json(rooms)
    rooms_name = {}
    for room in rooms:
        rooms_name[room["room_name"]] = {
            "room_id": room["room_id"],
            "capacity": room["capacity"]
        }
    # st.write(rooms_name)
    st.write("### 会議室一覧")
    df_rooms = pd.DataFrame(rooms)
    df_rooms.columns = ["会議室名", "定員", "会議室ID"]
    st.table(df_rooms)

    # 予約一覧取得
    url_bookings = api_base_url + "bookings/"
    bookings = requests.get(url_bookings).json()
    # st.json(bookings)

    users_id = {}
    for user in users:
        users_id[user["user_id"]] = user["username"]
    rooms_id = {}
    for room in rooms:
        rooms_id[room["room_id"]] = {
            "room_name": room["room_name"],
            "capacity": room["capacity"]
        }

    to_username = lambda x: users_id[x]
    to_room_name = lambda x: rooms_id[x]["room_name"]
    to_datetime = lambda x: datetime.datetime.fromisoformat(x).strftime("%Y/%m/%d %H:%M")

    st.write("### 予約一覧")
    df_bookings = pd.DataFrame(bookings)
    df_bookings['user_id'] = df_bookings['user_id'].map(to_username)
    df_bookings["room_id"] = df_bookings["room_id"].map(to_room_name)
    df_bookings["start_datetime"] = df_bookings["start_datetime"].map(to_datetime)
    df_bookings["end_datetime"] = df_bookings["end_datetime"].map(to_datetime)
    df_bookings = df_bookings.rename(columns={
        "user_id": "予約者名",
        "room_id": "会議室名",
        "booking_num": "予約人数",
        "start_datetime": "開始時刻",
        "end_datetime": "終了時刻",
        "boooking_id": "予約番号"
    })
    st.table(df_bookings)


    # withでFormを括る
    with st.form(key="room"):
        # booking_id: int = random.randint(0, 10)
        username: str = st.selectbox("予約者名", users_name.keys())
        room_name: str = st.selectbox("会議室名", rooms_name.keys())
        booked_num: int = st.number_input("予約人数", step=1, min_value=1)
        date = st.date_input("日付を入力", min_value=datetime.date.today())
        start_time = st.time_input("開始時刻", value=datetime.time(hour=9, minute=0))
        end_time = st.time_input("終了時刻", value=datetime.time(hour=start_time.hour+2, minute=start_time.minute))

        submit_botton = st.form_submit_button(label="会議室予約")

    if submit_botton:
        user_id: int = users_name[username]
        room_id: int = rooms_name[room_name]["room_id"]
        capacity: int = rooms_name[room_name]["capacity"]

        data = {
            # "booking_id": booking_id,
            "user_id": user_id,
            "room_id": room_id,
            "booked_num": booked_num,
            "start_datetime": datetime.datetime(
                year=date.year, 
                month=date.month, 
                day=date.day,
                hour=start_time.hour,
                minute=start_time.minute
            ).isoformat(),
            "end_datetime": datetime.datetime(
                year=date.year, 
                month=date.month, 
                day=date.day,
                hour=end_time.hour,
                minute=end_time.minute
            ).isoformat()
        }
        # 定員数のValidate
        if booked_num > capacity:
            st.error(f"{room_name}の定員は {capacity}名です。")
        # 開始時刻 >= 終了時刻
        elif start_time >= end_time:
            st.error(f"開始時刻が終了時刻を超えています。")
        # 開始時刻 >= 終了時刻
        elif start_time < datetime.time(hour=9, minute=0) or end_time > datetime.time(hour=20, minute=0):
            st.error(f"予約可能時間は9:00~20:00です。")
        
        else:
            url = api_base_url + "bookings/"
            res = requests.post(
                url,
                data = json.dumps(data)
            )
            if res.status_code == 200:
                st.success("予約完了しました")
            elif res.status_code == 404 and res.json()["detail"] == "予約重複":
                st.error("予約が重複しています")
            # st.json(res.json())
