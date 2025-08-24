import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Types
export interface User {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  is_verified: boolean;
  created_at: string;
}

export interface BusinessProfile {
  id: number;
  owner_id: number;
  business_name: string;
  business_description?: string;
  industry?: string;
  business_type?: string;
  founded_year?: number;
  employee_count?: number;
  annual_revenue?: number;
  email?: string;
  phone?: string;
  website?: string;
  street_address?: string;
  city?: string;
  state?: string;
  postal_code?: string;
  country?: string;
  linkedin_url?: string;
  twitter_url?: string;
  facebook_url?: string;
  instagram_url?: string;
  services_offered?: string[];
  target_market?: string;
  unique_selling_proposition?: string;
  business_model?: string;
  meta_title?: string;
  meta_description?: string;
  keywords?: string[];
  logo_url?: string;
  banner_image_url?: string;
  additional_images?: string[];
  is_published: boolean;
  is_featured: boolean;
  profile_slug?: string;
  created_at: string;
  updated_at: string;
}

export interface BusinessProfileCreate {
  business_name: string;
  business_description?: string;
  industry?: string;
  business_type?: string;
  founded_year?: number;
  employee_count?: number;
  annual_revenue?: number;
  email?: string;
  phone?: string;
  website?: string;
  street_address?: string;
  city?: string;
  state?: string;
  postal_code?: string;
  country?: string;
  linkedin_url?: string;
  twitter_url?: string;
  facebook_url?: string;
  instagram_url?: string;
  services_offered?: string[];
  target_market?: string;
  unique_selling_proposition?: string;
  business_model?: string;
  meta_title?: string;
  meta_description?: string;
  keywords?: string[];
}

export interface BusinessReview {
  id: number;
  business_id: number;
  reviewer_name: string;
  reviewer_email?: string;
  rating: number;
  review_text?: string;
  is_verified: boolean;
  is_published: boolean;
  created_at: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  user: User;
}

// Auth API
export const authApi = {
  login: async (email: string, password: string): Promise<LoginResponse> => {
    const formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);
    
    const response = await api.post('/auth/login', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  register: async (userData: {
    email: string;
    password: string;
    first_name: string;
    last_name: string;
  }): Promise<User> => {
    const response = await api.post('/auth/register', userData);
    return response.data;
  },

  getCurrentUser: async (): Promise<User> => {
    const response = await api.get('/auth/me');
    return response.data;
  },
};

// Business Profile API
export const businessProfileApi = {
  // User's profiles
  getUserProfiles: async (): Promise<BusinessProfile[]> => {
    const response = await api.get('/business-profiles/');
    return response.data;
  },

  getProfile: async (id: number): Promise<BusinessProfile> => {
    const response = await api.get(`/business-profiles/${id}`);
    return response.data;
  },

  createProfile: async (data: BusinessProfileCreate): Promise<BusinessProfile> => {
    const response = await api.post('/business-profiles/', data);
    return response.data;
  },

  updateProfile: async (id: number, data: Partial<BusinessProfileCreate>): Promise<BusinessProfile> => {
    const response = await api.put(`/business-profiles/${id}`, data);
    return response.data;
  },

  deleteProfile: async (id: number): Promise<void> => {
    await api.delete(`/business-profiles/${id}`);
  },

  uploadLogo: async (profileId: number, file: File): Promise<{ logo_url: string }> => {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await api.post(`/business-profiles/${profileId}/upload-logo`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  // Public profiles
  getPublicProfiles: async (params?: {
    skip?: number;
    limit?: number;
    industry?: string;
    city?: string;
    search?: string;
  }): Promise<BusinessProfile[]> => {
    const response = await api.get('/business-profiles/public', { params });
    return response.data;
  },

  getPublicProfile: async (slug: string): Promise<BusinessProfile> => {
    const response = await api.get(`/business-profiles/public/${slug}`);
    return response.data;
  },

  // Reviews
  getProfileReviews: async (profileId: number): Promise<BusinessReview[]> => {
    const response = await api.get(`/business-profiles/${profileId}/reviews`);
    return response.data;
  },

  createReview: async (profileId: number, reviewData: {
    reviewer_name: string;
    reviewer_email?: string;
    rating: number;
    review_text?: string;
  }): Promise<BusinessReview> => {
    const response = await api.post(`/business-profiles/${profileId}/reviews`, reviewData);
    return response.data;
  },
};

export default api;