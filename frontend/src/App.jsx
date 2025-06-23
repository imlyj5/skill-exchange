import React, { useState, useEffect } from "react";
import './App.css';
import axios from 'axios';
import LandingPage from './components/LandingPage/LandingPage';
import ProfilePage from './components/ProfilePage/ProfilePage';
import MatchSuggestionsPage from './components/MatchSuggestionsPage/MatchSuggestionsPage';
import ChatPage from './components/ChatPage/ChatPage';
import HowItWorksPage from './components/HowItWorksPage/HowItWorksPage';
import UserDropdown from './components/UserDropdown/UserDropdown';

export const API_URL = 'http://127.0.0.1:5000'; // Update to your Flask backend URL

const App = () => {
  const [user, setUser] = useState(null);
  const [page, setPage] = useState("landing");
  const [chats, setChats] = useState([]);
  const [selectedMatch, setSelectedMatch] = useState(null);
  const [viewedUser, setViewedUser] = useState(null);

  const fetchChats = (currentUserId) => {
    if (!currentUserId) return;
    axios.get(`${API_URL}/chats/${currentUserId}`)
      .then((response) => {
        // Handle new API response format: {"chats": [...]}
        const chatsData = response.data.chats || response.data || [];
        const transformedChats = chatsData.map(chat => {
          const isUser1 = chat.user1_id === currentUserId;
          const otherUserName = isUser1 ? chat.user2_name : chat.user1_name;
          const otherUserAvatar = isUser1 ? chat.user2_avatar : chat.user1_avatar;
          return {
            ...chat,
            name: otherUserName,
            avatar: otherUserAvatar,
            other_user: {
              id: isUser1 ? chat.user2_id : chat.user1_id,
              name: otherUserName,
              avatar: otherUserAvatar,
            },
          };
        });
        setChats(transformedChats);
      })
      .catch((err) => console.log("Error fetching chats:", err));
  };

  useEffect(() => {
    if (user && user.id) {
      fetchChats(user.id);
    } else {
      setChats([]);
      setSelectedMatch(null);
      setViewedUser(null);
    }
  }, [user]);

  useEffect(() => {
    if (!selectedMatch && chats && chats.length > 0) {
      const firstChatWithUnread = chats.find(c => c.unread_count > 0);
      setSelectedMatch(firstChatWithUnread || chats[0]);
    }
  }, [chats]);

  const handleLogin = (userData) => {
    const uid = userData.user_id || userData.id;
    if (uid) {
      axios.get(`${API_URL}/profile/${uid}`)
        .then((res) => {
          setUser(res.data);
          setPage('profile');
        })
        .catch((err) => {
          console.log("Error fetching profile:", err);
          setUser(userData);
          setPage('profile');
        });
    } else {
      setUser(userData);
      setPage('profile');
    }
  };

  const handleLogout = () => {
    setUser(null);
    setChats([]);
    setSelectedMatch(null);
    setViewedUser(null);
    setPage('landing');
  };

  const handleProfileSave = (profileData) => {
    setUser(profileData);
    fetchChats(profileData.id);
  };

  const handleSelectConversation = async (conversation) => {
    if (conversation.unread_count > 0) {
      try {
        await axios.put(`${API_URL}/chats/${conversation.id}/messages/read`, {
          user_id: user.id
        });
        setChats(prevChats =>
          prevChats.map(chat =>
            chat.id === conversation.id ? { ...chat, unread_count: 0 } : chat
          )
        );
      } catch (error) {
        console.error("Error marking messages as read:", error);
      }
    }
    setSelectedMatch(conversation);
  };

  const handleStartChat = async (matchUser) => {
    try {
      const existingChat = chats.find(chat => 
        (chat.user1_id === user.id && chat.user2_id === matchUser.id) ||
        (chat.user2_id === user.id && chat.user1_id === matchUser.id)
      );

      if (existingChat) {
        setSelectedMatch(existingChat);
        setPage('chat');
        return;
      }

      const response = await axios.post(`${API_URL}/chats`, {
        user1_id: user.id,
        user2_id: matchUser.id
      });

      const newChat = {
        ...response.data,
        name: matchUser.name,
        avatar: matchUser.avatar,
        other_user: {
          id: matchUser.id,
          name: matchUser.name,
          avatar: matchUser.avatar
        }
      };

      setChats(prevChats => [...prevChats, newChat]);
      setSelectedMatch(newChat);
      setPage('chat');
    } catch (error) {
      console.error("Error creating chat:", error);
      alert("Failed to start chat. Please try again.");
    }
  };

  const handleRatingSuccess = (ratedChatId) => {
    setChats(prevChats =>
      prevChats.map(chat =>
        chat.id === ratedChatId
          ? { ...chat, is_rated_by_current_user: true }
          : chat
      )
    );
  };

  const renderPage = () => {
    if (!user) {
      return <LandingPage onLogin={handleLogin} onSignup={handleLogin} onNavigate={setPage} />;
    }
    
    switch (page) {
      case 'howitworks':
        return <HowItWorksPage user={user} onLogin={handleLogin} onNavigate={setPage} onLogout={handleLogout} />;
      case 'landing':
        return <LandingPage onLogin={handleLogin} onNavigate={setPage} />;
      case 'profile':
        return <ProfilePage user={user} onSave={handleProfileSave} onNavigate={setPage} onLogout={handleLogout} />;
      case 'matches':
        return (
          <MatchSuggestionsPage
            onChat={handleStartChat}
            onNavigate={setPage}
            user={user}
            viewedUser={viewedUser}
            setViewedUser={setViewedUser}
            onLogout={handleLogout}
          />
        );
      case 'chat':
        return (
          <ChatPage
            match={selectedMatch}
            matches={chats}
            onSelectConversation={handleSelectConversation}
            onBack={() => setPage('matches')}
            user={user}
            onNavigate={setPage}
            onLogout={handleLogout}
            onRatingSuccess={handleRatingSuccess}
          />
        );
      default:
        return null;
    }
  };

  return (
    <div className="App">
      {renderPage()}
    </div>
  );
};

export default App;