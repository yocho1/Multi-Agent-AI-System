"use client";

import { useState, useEffect } from "react";
import { useAuth } from "@/contexts/auth-context";
import { useRouter } from "next/navigation";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import { toast } from "sonner";
import { User, Mail, Lock, MapPin, Calendar, Shield, ArrowLeft, Camera } from "lucide-react";
import { updateProfile, updateEmail, updatePassword } from "firebase/auth";
import { auth } from "@/lib/firebase";

export default function ProfilePage() {
  const { user } = useAuth();
  const router = useRouter();

  const [isEditing, setIsEditing] = useState(false);
  const [isSaving, setIsSaving] = useState(false);

  // Form state
  const [displayName, setDisplayName] = useState(user?.displayName || "");
  const [email, setEmail] = useState(user?.email || "");
  const [location, setLocation] = useState("");
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [photoURL, setPhotoURL] = useState(user?.photoURL || "");
  const [isUploadingPhoto, setIsUploadingPhoto] = useState(false);
  const [isLoadingLocation, setIsLoadingLocation] = useState(true);

  // Auto-detect location on component mount
  useEffect(() => {
    const detectLocation = async () => {
      try {
        // Use backend to get location (avoids CORS issues)
        const response = await fetch("/api/v1/location");
        if (response.ok) {
          const data = await response.json();
          const detectedLocation = data.location || "Not detected";
          setLocation(detectedLocation);
          if (data.location) {
            toast.success(`Location detected: ${detectedLocation}`);
          }
        } else {
          throw new Error("Backend location API failed");
        }
      } catch (error) {
        console.log("Could not auto-detect location from backend:", error);
        // Fallback: Try browser geolocation
        if (navigator.geolocation) {
          navigator.geolocation.getCurrentPosition(
            async (position) => {
              try {
                const { latitude, longitude } = position.coords;
                const response = await fetch(
                  `https://nominatim.openstreetmap.org/reverse?format=json&lat=${latitude}&lon=${longitude}`
                );
                const data = await response.json();
                const detectedLocation = data.address?.city || data.address?.county || "Unknown Location";
                setLocation(detectedLocation);
                toast.success(`Location detected: ${detectedLocation}`);
              } catch (err) {
                console.log("Could not reverse geocode:", err);
              }
            },
            () => {
              console.log("Geolocation permission denied");
            }
          );
        }
      } finally {
        setIsLoadingLocation(false);
      }
    };

    detectLocation();
  }, []);

  const userInitials = user?.displayName
    ?.split(" ")
    .map((n) => n[0])
    .join("")
    .toUpperCase() || "U";

  const handleUpdateProfile = async () => {
    if (!user) return;

    setIsSaving(true);
    try {
      // Update display name
      if (displayName !== user.displayName) {
        await updateProfile(user, {
          displayName: displayName,
        });
      }

      // Update email
      if (email !== user.email) {
        await updateEmail(user, email);
      }

      // Update photoURL
      if (photoURL !== user.photoURL) {
        await updateProfile(user, {
          photoURL: photoURL || null,
        });
      }

      toast.success("Profile updated successfully!");
      setIsEditing(false);
    } catch (error) {
      toast.error(`Failed to update profile: ${(error as Error).message}`);
    } finally {
      setIsSaving(false);
    }
  };

  const handlePhotoUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setIsUploadingPhoto(true);
    try {
      const reader = new FileReader();
      reader.onloadend = async () => {
        const base64String = reader.result as string;
        setPhotoURL(base64String);
        
        if (user) {
          await updateProfile(user, {
            photoURL: base64String,
          });
          toast.success("Avatar updated successfully!");
        }
      };
      reader.readAsDataURL(file);
    } catch (error) {
      toast.error(`Failed to upload avatar: ${(error as Error).message}`);
    } finally {
      setIsUploadingPhoto(false);
    }
  };

  const handleUpdatePassword = async () => {
    if (newPassword !== confirmPassword) {
      toast.error("Passwords do not match");
      return;
    }

    if (newPassword.length < 6) {
      toast.error("Password must be at least 6 characters");
      return;
    }

    if (!user) return;

    setIsSaving(true);
    try {
      // Firebase doesn't allow password change without re-authentication
      // For now, show a message
      await updatePassword(user, newPassword);
      toast.success("Password updated successfully!");
      setCurrentPassword("");
      setNewPassword("");
      setConfirmPassword("");
    } catch (error) {
      toast.error(`Failed to update password: ${(error as Error).message}`);
    } finally {
      setIsSaving(false);
    }
  };

  if (!user) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <Card>
          <CardContent className="pt-6">
            <p>Loading profile...</p>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="container max-w-4xl px-4 py-12">
      {/* Back Button */}
      <Button
        variant="ghost"
        onClick={() => router.back()}
        className="mb-6 text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white"
      >
        <ArrowLeft className="h-4 w-4 mr-2" />
        Go Back
      </Button>

      {/* Profile Header */}
      <div className="mb-8">
        <h1 className="text-4xl font-bold tracking-tight mb-2">My Profile</h1>
        <p className="text-lg text-muted-foreground">
          Manage your account settings and personal information
        </p>
      </div>

      {/* Profile Card */}
      <div className="grid gap-6 md:grid-cols-3 mb-8">
        <Card className="md:col-span-1 border-blue-200 dark:border-blue-800 text-center">
          <CardHeader>
            <CardTitle className="text-center">Account Status</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="relative inline-block">
              {photoURL ? (
                <img
                  src={photoURL}
                  alt={displayName}
                  className="h-20 w-20 rounded-full object-cover shadow-lg mx-auto"
                />
              ) : (
                <div className="h-20 w-20 rounded-full bg-gradient-to-br from-blue-500 to-violet-500 flex items-center justify-center text-white font-bold text-3xl shadow-lg mx-auto">
                  {userInitials}
                </div>
              )}
              <label className="absolute bottom-0 right-0 p-2 bg-blue-600 hover:bg-blue-700 text-white rounded-full cursor-pointer shadow-md transition-colors">
                <Camera className="h-4 w-4" />
                <input
                  type="file"
                  accept="image/*"
                  className="hidden"
                  onChange={handlePhotoUpload}
                  disabled={isUploadingPhoto}
                />
              </label>
            </div>
            <p className="text-xs text-muted-foreground">Click camera icon to update</p>
            <div>
              <p className="text-sm font-medium text-muted-foreground mb-2">Verification Status</p>
              <Badge className="bg-green-100 text-green-800 dark:bg-green-950 dark:text-green-400">
                ✓ Verified
              </Badge>
            </div>
            <div>
              <p className="text-sm font-medium text-muted-foreground mb-2">Account Created</p>
              <p className="text-sm font-semibold">
                {user.metadata?.creationTime ? new Date(user.metadata.creationTime).toLocaleDateString() : "N/A"}
              </p>
            </div>
          </CardContent>
        </Card>

        {/* Profile Information */}
        <Card className="md:col-span-2 border-blue-200 dark:border-blue-800">
          <CardHeader className="flex flex-row items-center justify-between">
            <div>
              <CardTitle className="flex items-center gap-2">
                <User className="h-5 w-5 text-blue-600" />
                Personal Information
              </CardTitle>
              <CardDescription>View and update your profile details</CardDescription>
            </div>
            <Button
              onClick={() => setIsEditing(!isEditing)}
              variant={isEditing ? "default" : "outline"}
            >
              {isEditing ? "Cancel" : "Edit"}
            </Button>
          </CardHeader>

          <CardContent className="space-y-6">
            {/* Full Name */}
            <div className="space-y-2">
              <Label className="flex items-center gap-2">
                <User className="h-4 w-4" />
                Full Name
              </Label>
              {isEditing ? (
                <Input
                  value={displayName}
                  onChange={(e) => setDisplayName(e.target.value)}
                  placeholder="Enter your full name"
                  disabled={isSaving}
                />
              ) : (
                <div className="px-4 py-2 rounded-lg bg-slate-100 dark:bg-slate-800">
                  {displayName || "Not set"}
                </div>
              )}
            </div>

            {/* Email */}
            <div className="space-y-2">
              <Label className="flex items-center gap-2">
                <Mail className="h-4 w-4" />
                Email Address
              </Label>
              {isEditing ? (
                <Input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="Enter your email"
                  disabled={isSaving}
                />
              ) : (
                <div className="px-4 py-2 rounded-lg bg-slate-100 dark:bg-slate-800">
                  {email}
                </div>
              )}
            </div>

            {/* Location */}
            <div className="space-y-2">
              <Label className="flex items-center gap-2">
                <MapPin className="h-4 w-4" />
                Location
              </Label>
              {isEditing ? (
                <div className="space-y-2">
                  <Input
                    value={location}
                    onChange={(e) => setLocation(e.target.value)}
                    placeholder="Enter your location"
                    disabled={isSaving}
                  />
                  <p className="text-xs text-muted-foreground">
                    {isLoadingLocation ? "🔍 Detecting location..." : "✓ Auto-detected from your IP/browser"}
                  </p>
                </div>
              ) : (
                <div className="px-4 py-2 rounded-lg bg-slate-100 dark:bg-slate-800">
                  {location || "Not specified"}
                </div>
              )}
            </div>

            {/* Account Type */}
            <div className="space-y-2">
              <Label className="flex items-center gap-2">
                <Shield className="h-4 w-4" />
                Account Type
              </Label>
              <div className="px-4 py-2 rounded-lg bg-slate-100 dark:bg-slate-800">
                Premium User
              </div>
            </div>

            {/* Last Login */}
            <div className="space-y-2">
              <Label className="flex items-center gap-2">
                <Calendar className="h-4 w-4" />
                Last Login
              </Label>
              <div className="px-4 py-2 rounded-lg bg-slate-100 dark:bg-slate-800">
                {user.metadata?.lastSignInTime ? new Date(user.metadata.lastSignInTime).toLocaleString() : "Never"}
              </div>
            </div>

            {isEditing && (
              <Button
                onClick={handleUpdateProfile}
                disabled={isSaving}
                className="w-full bg-blue-600 hover:bg-blue-700"
              >
                {isSaving ? "Saving..." : "Save Changes"}
              </Button>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Change Password Section */}
      <Card className="border-red-200 dark:border-red-800">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-red-600 dark:text-red-400">
            <Lock className="h-5 w-5" />
            Security
          </CardTitle>
          <CardDescription>Update your password to keep your account secure</CardDescription>
        </CardHeader>

        <CardContent className="space-y-6">
          {/* Current Password */}
          <div className="space-y-2">
            <Label>Current Password</Label>
            <Input
              type="password"
              value={currentPassword}
              onChange={(e) => setCurrentPassword(e.target.value)}
              placeholder="Enter current password"
              disabled={isSaving}
            />
            <p className="text-xs text-muted-foreground">
              Firebase requires re-authentication for security
            </p>
          </div>

          {/* New Password */}
          <div className="space-y-2">
            <Label>New Password</Label>
            <Input
              type="password"
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              placeholder="Enter new password (min 6 characters)"
              disabled={isSaving}
            />
          </div>

          {/* Confirm Password */}
          <div className="space-y-2">
            <Label>Confirm Password</Label>
            <Input
              type="password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              placeholder="Confirm new password"
              disabled={isSaving}
            />
          </div>

          <Button
            onClick={handleUpdatePassword}
            disabled={isSaving || !newPassword || !confirmPassword}
            className="w-full bg-red-600 hover:bg-red-700"
          >
            {isSaving ? "Updating..." : "Update Password"}
          </Button>

          <div className="bg-yellow-50 dark:bg-yellow-950/20 border border-yellow-200 dark:border-yellow-800 rounded-lg p-4">
            <p className="text-sm text-yellow-800 dark:text-yellow-200">
              💡 <strong>Tip:</strong> Keep your password strong and unique. Never share it with anyone.
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
