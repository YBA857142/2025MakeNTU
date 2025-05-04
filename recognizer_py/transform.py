import numpy as np
import cv2

def solve_homography(u, v):
    """
    This function should return a 3-by-3 homography matrix,
    u, v are N-by-2 matrices, representing N corresponding points for v = T(u)
    :param u: N-by-2 source pixel location matrices
    :param v: N-by-2 destination pixel location matrices
    :return:
    """
    u, v = v, u
    N = u.shape[0]
    H = None

    if v.shape[0] is not N:
        print('u and v should have the same size')
        return None
    if N < 4:
        print('At least 4 points should be given')

    # TODO: 1.forming A
    A = np.zeros((2 * N, 9))
    for i in range(N):
        A[2 * i, :] = np.array([u[i, 0], u[i, 1], 1, 0, 0, 0, -u[i, 0] * v[i, 0], -u[i, 1] * v[i, 0], -v[i, 0]])
        A[2 * i + 1, :] = np.array([0, 0, 0, u[i, 0], u[i, 1], 1, -u[i, 0] * v[i, 1], -u[i, 1] * v[i, 1], -v[i, 1]])
        
    # TODO: 2.solve H with A
    _, _, V = np.linalg.svd(A)
    H = V[-1, :].reshape((3, 3))

    return H


def warping(src, H, ymin, ymax, xmin, xmax):
    h_src, w_src, ch = src.shape
    H_inv = np.linalg.inv(H)

    dst = np.zeros((ymax - ymin, xmax - xmin, ch), dtype=src.dtype)

    # TODO: 1.meshgrid the (x,y) coordinate pairs
    Ux, Uy = np.meshgrid(np.arange(xmin, xmax), np.arange(ymin, ymax))

    # TODO: 2.reshape the destination pixels as N x 3 homogeneous coordinate
    U = np.vstack((Ux.flatten(), Uy.flatten(), np.ones((1, Ux.size)))).T

    # TODO: 3.apply H_inv to the destination pixels and retrieve (u,v) pixels, then reshape to (ymax-ymin),(xmax-xmin)
    V = np.dot(H_inv, U.T)
    V = V/V[2]
    Vx = V[0].reshape((ymax - ymin, xmax - xmin))
    Vy = V[1].reshape((ymax - ymin, xmax - xmin))

    # TODO: 4.calculate the mask of the transformed coordinate (should not exceed the boundaries of source image)
    mask = (Vx >= 0) & (Vx < w_src - 1) & (Vy >= 0) & (Vy < h_src - 1)

    # TODO: 5.sample the source image with the masked and reshaped transformed coordinates
    Vx = Vx[mask]
    Vy = Vy[mask]
    Vx_int = Vx.astype(int)
    Vy_int = Vy.astype(int)

    dVx = (Vx - Vx_int).reshape(-1, 1)
    dVy = (Vy - Vy_int).reshape(-1, 1)

    src[Vy_int, Vx_int]

    interpolated = np.zeros((h_src, w_src, ch))
    interpolated[Vy_int, Vx_int] += (1 - dVx) * (1 - dVy) * src[Vy_int, Vx_int]
    interpolated[Vy_int, Vx_int] += dVx * (1 - dVy) * src[Vy_int, Vx_int + 1]
    interpolated[Vy_int, Vx_int] += (1 - dVx) * dVy * src[Vy_int + 1, Vx_int]
    interpolated[Vy_int, Vx_int] += dVx * dVy * src[Vy_int + 1, Vx_int + 1]
    
    # TODO: 6. assign to destination image with proper masking
    dst[ymin:ymax, xmin:xmax][mask] = interpolated[Vy_int, Vx_int]

    return dst 

def transform(img, corners):
    """ 
    given a source image, a target canvas and the indicated corners, warp the source image to the target canvas
    :param img: input source image
    :param canvas: input canvas image
    :param corners: shape (4,2) numpy array, representing the four image corner (x, y) pairs
    :return: warped output image
    """
    h, w, ch = img.shape
    x = np.array([[0, 0],
                  [w, 0],
                  [w, h],
                  [0, h]
                  ])
    H = solve_homography(x, corners)
    
    return  warping(img, H, 0, h, 0, w)


if __name__ == "__main__":

    # ================== Part 1: Homography Estimation ========================

    # TODO: 1.you can use whatever images you like, include these images in the img directory
    img = cv2.imread('./data_imgs/pos/img0.webp')
    img = cv2.resize(img, (192, 256))

    # canvas_corners1 = np.array([[0, 150], [600, 0], [600, 600], [0, 450]])

    pts_src = np.float32([[64, 0], [128, 0], [192, 256], [0, 256]])

    # Step 2: Define destination rectangle (e.g., 300x300)
    pts_dst = np.float32([[0, 0], [192, 0], [192, 256], [0, 256]])

    # Step 3: Compute homography matrix to warp to rectangle
    H, _ = cv2.findHomography(pts_src, pts_dst)

    # Step 4: Warp the image to rectified rectangle
    warped = cv2.warpPerspective(img, H, (192, 256))

    # Step 5: Reverse the homography
    H_inv = np.linalg.inv(H)

    # Warp back to the original image shape
    recovered = cv2.warpPerspective(warped, H_inv, (192, 256))

    # Step 6: Display the images
    cv2.imwrite('warped.jpg', warped)