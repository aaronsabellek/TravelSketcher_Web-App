export interface Destination {
    id: string;
    img_link: string;
    title: string;
    country: string;
    status: string;
    tags: string;
    free_text: string;
}

export interface Activity {
    id: string;
    img_link: string;
    title: string;
    status: string;
    tags: string;
    free_text: string;
    web_link: string;
    destination_id: string;
}

export interface UserProfile {
    id: string;
    username: string;
    email: string;
    password: string;
    city: string;
    country: string | null;
}

export interface UnsplashImage {
id: string;
url: string;
alt_description: string;
}